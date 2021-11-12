import argparse
import binascii
import socket
import sys
import threading
import urllib.parse
import json
import time
import hashlib
import struct


def sha256d(message):
    return hashlib.sha256(hashlib.sha256(message).digest()).digest()


def swap_endian_word(hex_word):
    message = binascii.unhexlify(hex_word)

    if len(message) != 4:
        raise ValueError('В слове должно быть 4 байта!')

    return message[::-1]


def swap_endian_words(hex_words):
    message = binascii.unhexlify(hex_words)

    if len(message) % 4 != 0:
        raise ValueError('В слове должно быть %4 байтов!')

    tmp = b''
    for i in range(0, len(message) // 4):
        tmp = tmp + message[4 * i: 4 * i + 4][::-1]
    return tmp


def human_readable_hashrate(hashrate):
    if hashrate < 1000:
        return '%2f h/s' % hashrate
    if hashrate < 1000000:
        return '%2f Kh/s' % (hashrate / 1000)
    if hashrate < 1000000000:
        return '%2f Mh/s' % (hashrate / 1000000)
    return '%2f Gh/s' % (hashrate / 1000000000)


class Job(object):
    def __init__(self, job_id, prevhash, coinb1, coinb2,
                 merkle_branches, version, nbits, ntime, target, extranounce1, extranounce2_size):
        self._job_id = job_id
        self._prevhash = prevhash
        self._coinb1 = coinb1
        self._coinb2 = coinb2
        self._merkle_branches = [b for b in merkle_branches]
        self._version = version
        self._nbits = nbits
        self._ntime = ntime

        self._target = target
        self._extranounce1 = extranounce1
        self._extranounce2_size = extranounce2_size

        self._done = False

        self._dt = 0.0
        self._hash_count = 0

    def stop(self):
        self._done = True

    @property
    def hashrate(self):
        if self._dt == 0:
            return 0.0

        return self._hash_count / self._dt

    def merkle_root_bin(self, extranounce2_bin):
        coinbase_bin = binascii.unhexlify(self._coinb1) + binascii.unhexlify(self._extranounce1) + extranounce2_bin + \
                       binascii.unhexlify(self._coinb2)
        coinbase_hash_bin = sha256d(coinbase_bin)

        merkle_root = coinbase_hash_bin
        for branch in self._merkle_branches:
            merkle_root = sha256d(merkle_root + binascii.unhexlify(branch))
        return merkle_root

    def mining(self, nounce_start=0, nounce_stride=1):
        t0 = time.time()

        for extranounce2 in range(1, 0xffffffff):
            extranounce2_bin = struct.pack('>I', extranounce2)

            merkle_root_bin = self.merkle_root_bin(extranounce2_bin)

            header_prefix_bin = swap_endian_word(self._version) + swap_endian_words(self._prevhash) + \
                                merkle_root_bin + swap_endian_word(self._ntime) + swap_endian_word(self._nbits)

            for nounce in range(nounce_start, 0xffffffff, nounce_stride):
                if self._done:
                    self._dt += (time.time() - t0)
                    raise StopIteration()

                nounce_bin = struct.pack('<I', nounce)
                work_proof = sha256d(header_prefix_bin + nounce_bin)[::-1].hex()
                # print(work_proof)

                self._hash_count += 1

                if work_proof <= self._target:
                    result = dict(
                        job_id=self._job_id,
                        extranounce2=extranounce2_bin.hex(),
                        ntime=self._ntime,
                        nounce=nounce_bin[::-1].hex()
                    )

                    yield result

                    self._dt += (time.time() - t0)
                    t0 = time.time()
                    self._hash_count = 0


class Subscription(object):
    def __init__(self):
        self._id = None
        self._difficulty = None
        self._extranounce1 = None
        self._extranounce2_size = None
        self._target = None
        self._worker_name = None
        self._mining_thread = None

    class SubscriptionException(Exception):
        pass

    def set_subscription(self, subscription_id_tmp, extranounce1_tmp, extranounce2_size_tmp):
        if self._id is not None:
            raise self.SubscriptionException('ID подписки, возвращенный майнинг-пулом, был получен！')

        self._id = subscription_id_tmp
        self._extranounce1 = extranounce1_tmp
        self._extranounce2_size = extranounce2_size_tmp

    def set_worker_name(self, worker_name_tmp):
        if self._worker_name:
            raise self.SubscriptionException('Вы уже авторизовались в майнинг-пуле под своим именем пользователя！')

        self._worker_name = worker_name_tmp

    def get_worker_name(self):
        return self._worker_name

    def set_target(self, difficulty):
        if difficulty < 0:
            raise self.SubscriptionException('Установлена отрицательная сложность！')

        if difficulty == 0:
            target = 2 ** 256 - 1
        else:
            target = min(int((0xffff0000 * 2 ** (256 - 64) + 1) / difficulty - 1 + 0.5), 2 ** 256 - 1)
        self._target = '%064x' % target
        self._difficulty = difficulty

        print('Текущая сложность：', self._difficulty)

    def create_job(self, job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime):

        if self._id is None:
            raise self.SubscriptionException('Подписка не выполнена！')

        return Job(
            job_id=job_id,
            prevhash=prevhash,
            coinb1=coinb1,
            coinb2=coinb2,
            merkle_branches=merkle_branches,
            version=version,
            nbits=nbits,
            ntime=ntime,
            target=self._target,
            extranounce1=self._extranounce1,
            extranounce2_size=self._extranounce2_size
        )


class Client(object):
    def __init__(self):
        self._socket = None
        self._lock = threading.RLock()
        self._rpc_thread = None
        self._message_id = 1
        self._requests = dict()

    class ClientException(Exception):
        pass

    def connect(self, socket_tmp):
        if self._rpc_thread:
            raise self.ClientException('Майнинг пул подключен！')

        self._socket = socket_tmp

        self._rpc_thread = threading.Thread(target=self._handle_incoming_rpc)
        self._rpc_thread.daemon = True
        self._rpc_thread.start()

    def send(self, method, params):
        if not self._socket:
            raise self.ClientException('Не подключено')

        request = dict(id=self._message_id, method=method, params=params)

        message = json.dumps(request)
        with self._lock:
            self._requests[self._message_id] = request
            self._message_id += 1
            self._socket.send((message + '\n').encode())

        # print(message)

        return request

    def _handle_incoming_rpc(self):
        data = ""

        while True:
            if '\n' in data:
                (line, data) = data.split('\n', 1)
            else:
                chunk = self._socket.recv(1024)
                data += chunk.decode()
                continue

            try:
                reply = json.loads(line)
                # print(reply)
            except IOError:
                print('Не удалось преобразовать данные TCP в формат JSON！')
                continue

            try:
                request = None
                with self._lock:
                    if 'id' in reply and reply['id'] in self._requests:
                        request = self._requests[reply['id']]
                    self.handle_reply(request=request, reply=reply)
            except IOError:
                print("Возвращенное сообщение не соответствует содержанию сообщения запроса!")
                continue

    def handle_reply(self, request, reply):
        pass


class Mining(Client):
    def __init__(self, url, username, password):
        Client.__init__(self)

        self._url = url
        self._username = username
        self._password = password
        self._job = None
        self._accepted_shares = 0
        self._subscription = Subscription()
        self._login = 0
        self._login_first_job = 0
        self._change_difficulty_first_job = 0
        self.kf = 0.00000001

    def mining_forever(self):
        url = urllib.parse.urlparse(self._url)
        hostname = url.hostname
        port = url.port
        # print(hostname, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        self.connect(sock)

        self.send(method='mining.subscribe', params=[])

        while True:
            #kf = hashlib.deposit(self.kf)
            time.sleep(10)

    def handle_reply(self, request, reply):
        # if self._login == 1:

        if reply.get('method') == 'mining.set_difficulty':
            if 'params' not in reply or len(reply['params']) != 1:
                print('Неправильный формат ответа на изменение сложности майнинг-пула！')

            (difficulty,) = reply['params']

            self._subscription.set_target(difficulty)

            self._change_difficulty_first_job = 0

            print('Успешно завершено изменение сложности и расчет задачи!')

        elif reply.get('method') == 'mining.notify':
            if 'params' not in reply or len(reply['params']) != 9:
                print('Неправильный формат задачи майнинга, возвращаемой пулом майнинга!')

            (job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime, clean_jobs) = reply['params']

            if self._login == 1 and self._login_first_job == 0:
                self.mining_job_thread(job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime)

                self._login_first_job = 1
                self._change_difficulty_first_job = 1

                print('Вход в систему завершен, запуск потока майнинга')

            elif self._login == 1 and self._change_difficulty_first_job == 0:
                self.mining_job_thread(job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime)

                self._login_first_job = 1
                self._change_difficulty_first_job = 1

                print('Сложность изменена, запуск потока майнинга')

            elif self._login == 1 and clean_jobs:
                self.mining_job_thread(job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime)

                self._login_first_job = 1
                self._change_difficulty_first_job = 1

                print('Принудительно запущен поток майнинга!')

        elif request:
            if request.get('method') == 'mining.subscribe':
                if 'result' not in reply or len(reply['result']) != 3 or len(reply['result'][0]) != 2:
                    print('Вход в систему завершен, запуск потока майнинга')

                ((mining_notify, mining_difficulty), extranounce1, extranounce2_size) = reply['result']

                self._subscription.set_subscription(mining_notify[1], extranounce1, extranounce2_size)

                print('Успешно подписано!')

                self.send(method='mining.authorize', params=[self._username, self._password])

            elif request.get('method') == 'mining.authorize':
                if 'result' not in reply or not reply['result']:
                    print('Майнинг пул отказал во входе в учетную запись！')

                worker_name = request['params'][0]

                self._subscription.set_worker_name(worker_name)

                self._login = 1
                self._login_first_job = 0

                print('Вход в учетную запись успешен!')

            elif request.get('method') == 'mining.submit':
                if 'result' not in reply or not reply['result']:
                    print('Майнинг пул отклонил результат отправки！')
                    print(reply)

                else:
                    self._accepted_shares += 1
                    print('Успешно отправлен результат отправки! Общее количество результатов отправки：',
                          self._accepted_shares)

    def mining_job_thread(self, job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime):

        if self._job:
            self._job.stop()
            print('Старая работа завершена')

        self._job = self._subscription.create_job(
            job_id=job_id,
            prevhash=prevhash,
            coinb1=coinb1,
            coinb2=coinb2,
            merkle_branches=merkle_branches,
            version=version,
            nbits=nbits,
            ntime=ntime
        )

        def run(job):
            try:
                for result in job.mining():
                    params = [self._subscription.get_worker_name()] + [result[k] for k in ('job_id', 'extranounce2',
                                                                                           'ntime', 'nounce')]
                    self.send(method='mining.submit', params=params)
                    print("Старая работа завершена！: " + str(params))
                    print(human_readable_hashrate(job.hashrate))
            except IOError:
                print('Ошибка при отправке результатов！')

        thread = threading.Thread(target=run, args=(self._job,))
        thread.daemon = True
        thread.start()


class NoWalletSet(Exception):
    pass


class Implementation:
    def __init__(self):
        file = open('settings.txt', 'r')
        data = file.readlines()
        bitcoinkey = ''
        if len(data) >= 5:
            bitcoinkey = data[4].strip()
            bitcoinkey = bitcoinkey[bitcoinkey.find('=') + 1:]
        else:
            raise NoWalletSet
        if not bitcoinkey:
            raise NoWalletSet
        file.close()
        optionsurl = 'stratum+tcp://sha256.eu-north.nicehash.com:3334'
        optionsusername = bitcoinkey
        optionspassword = 'x'

        if optionsurl:
            mining = Mining(optionsurl, optionsusername, optionspassword)
            mining.mining_forever()
