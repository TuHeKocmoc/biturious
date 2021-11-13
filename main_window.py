import sys
import re
import string
import uuid
import os
import hashlib
import sqlite3
import pathlib
import datetime


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5 import QtWidgets, QtGui, QtCore
from parse import parse
from menu_script import Menu
from PyQt5.QtCore import Qt, QThread
from miner import Implementation
from main_win import Ui_MainWindow as Ui_Main

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def check_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email)


def check_pass(test_str):
    allowed = set(string.digits + string.ascii_letters)
    return set(test_str) <= allowed


def hash_password(password):
    salt = uuid.uuid4().hex
    os.environ['SALT'] = 'bK4-LbL-fT7-2WB'
    res = hashlib.sha512(os.getenv('SALT').encode() + salt.encode() + password.encode()).hexdigest() + ':' + salt
    os.environ.clear()
    return res


class External(QThread):
    """
    Runs a thread.
    """
    def __init__(self, *args):
        super().__init__()
        self.window = args[0]
        
    def run(self):
        try:
            Implementation()
        except:
            font = QtGui.QFont()
            font.setPointSize(10)
            self.window.label_2.setFont(font)
            self.window.label_2.setText('Кошелек не указан')
            self.window.switch.setCheckState(False)
            self.window.label_2.move(83, 130)
            self.window.label_2.resize(135, 25)


class MainWindow(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plainTextEdit_3.insertPlainText(parse())
        self.thread = External(self)
        self.initUI()
        con = sqlite3.connect("auth.db")
        cur = con.cursor()
        if os.path.exists('settings.txt'):
            file = open('settings.txt', 'r')
            logpass = file.readlines()
            login = logpass[0].strip()
            password = logpass[1].strip()
            self.login = login[login.find('=') + 1:]
            self.password = password[password.find('=') + 1:]
            file.close()
        else:
            self.login = 'ERROR'
            self.password = 'ERROR'
        self.lineEdit.setText(self.login)
        email = cur.execute("""SELECT email FROM users WHERE login = ? """, (self.login,)).fetchall()
        self.email = email[0][0]
        self.lineEdit_2.setText(self.email)
        self.lineEdit_3.setText(self.password)
        self.pushButton_3.clicked.connect(self.restore_txt)
        self.pushButton_2.clicked.connect(self.check)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_3.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_4.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_5.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_6.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        file = open('settings.txt', 'r')
        data = file.readlines()
        self.apikey = ''
        self.secretkey = ''
        self.bitcoinkey = ''
        if len(data) >= 3:
            apikey = data[2].strip()
            self.apikey = apikey[apikey.find('=') + 1:]
            self.lineEdit_4.setText(self.apikey)
        if len(data) >= 4:
            secretkey = data[3].strip()
            self.secretkey = secretkey[secretkey.find('=') + 1:]
            self.lineEdit_5.setText(self.secretkey)
        if len(data) >= 5:
            bitcoinkey = data[4].strip()
            self.bitcoinkey = bitcoinkey[bitcoinkey.find('=') + 1:]
            self.lineEdit_6.setText(self.bitcoinkey)
        file.close()

    def initUI(self):
        self.move(500, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.switch = QtWidgets.QCheckBox(self)
        self.switch.setStyleSheet('''
            QCheckBox::indicator:unchecked {
                image: url(off.png);
            }
            QCheckBox::indicator:checked {
                image: url(on.png);
            } 
            QCheckBox::indicator {
                background-color: rgb(46, 52, 54)
            }
        ''')
        self.switch.adjustSize()
        self.switch.move(110, 60)
        self.switch.resize(80, 40)
        self.pushButton.clicked.connect(self.menu)
        self.wrap.clicked.connect(self.rollup)
        self.exit.clicked.connect(self.my_close)
        self.switch.clicked.connect(self.yes_or_no)

    def menu(self):
        self.second_form = Menu(self)
        self.second_form.show()
        self.close()

    def yes_or_no(self):
        sender: QCheckBox = self.sender()
        if sender.isChecked():
            self.label_2.setText('Работает')
            self.label_2.move(100, 130)
            self.label_2.resize(131, 25)
            self.thread.start()

        else:
            self.thread.terminate()
            self.label_2.setText('Не работает')
            self.label_2.move(83, 130)
            self.label_2.resize(135, 25)

    def rollup(self):
        self.showMinimized()

    def my_close(self):
        self.close()

    def restore_txt(self):
        con = sqlite3.connect("auth.db")
        cur = con.cursor()
        file = open('settings.txt', 'r')
        logpass = file.readlines()
        login = logpass[0].strip()
        password = logpass[1].strip()
        self.login = login[login.find('=') + 1:]
        self.password = password[password.find('=') + 1:]
        file.close()
        self.lineEdit.setText(self.login)
        email = cur.execute("""SELECT email FROM users WHERE login = ? """, (self.login,)).fetchall()
        self.email = email[0][0]
        self.lineEdit_2.setText(self.email)
        self.lineEdit_3.setText(self.password)
        file = open('settings.txt', 'r')
        data = file.readlines()
        self.apikey = ''
        self.secretkey = ''
        self.bitcoinkey = ''
        if len(data) >= 3:
            apikey = data[2].strip()
            self.apikey = apikey[apikey.find('=') + 1:]
            self.lineEdit_4.setText(self.apikey)
        if len(data) >= 4:
            secretkey = data[3].strip()
            self.secretkey = secretkey[secretkey.find('=') + 1:]
            self.lineEdit_5.setText(self.secretkey)
        if len(data) >= 5:
            bitcoinkey = data[4].strip()
            self.bitcoinkey = bitcoinkey[bitcoinkey.find('=') + 1:]
            self.lineEdit_6.setText(self.bitcoinkey)
        file.close()

    def check(self):
        self.lineEdit.setText(self.login)
        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        if self.lineEdit_2.text() != self.email:
            self.email = self.lineEdit_2.text()
            if not self.email:
                self.lineEdit.setText('Вы не ввели почту!')
                con.close()
                return 0
            elif not check_email(self.email):
                self.lineEdit.setText('Вы ввели неверную почту')
                con.close()
                return 0

            true_email = cur.execute("""SELECT email FROM users 
                             WHERE login = ? """, (self.login,)).fetchall()

            cur.execute("INSERT INTO password_changes(user, time, old_password, new_password) VALUES(?, ?, ?, ?)",
                        (self.login, datetime.datetime.now(), true_email[0][0], self.email))

            cur.execute("""UPDATE users 
                            SET email = ? 
                            WHERE login = ?""", (self.email, self.login))

        if self.lineEdit_3.text() != self.password:
            self.password = self.lineEdit_3.text()
            if not self.password:
                self.lineEdit.setText('Вы не ввели пароль!')
                con.close()
                return 0

            elif not check_pass(self.password):
                self.lineEdit.setText('Пароль содержит запрещенные символы')
                con.close()
                return 0

            true_password = cur.execute("""SELECT password FROM users 
                             WHERE login = ? """, (self.login,)).fetchall()

            cur.execute("INSERT INTO password_changes(user, time, old_password, new_password) VALUES(?, ?, ?, ?)",
                        (self.login, datetime.datetime.now(), true_password[0][0], hash_password(self.password)))

            cur.execute("""UPDATE users 
                            SET password = ? 
                            WHERE email = ?""", (hash_password(self.password), self.login))

            file = open('settings.txt', 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open('settings.txt', 'w+')
            list_strings[1] = 'password=' + self.password
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')

        if self.lineEdit_4.text() != self.apikey:
            file = open('settings.txt', 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open('settings.txt', 'w+')
            list_strings[2] = 'apikey=' + self.lineEdit_4.text()
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')
            file.close()

        if self.lineEdit_5.text() != self.secretkey:
            file = open('settings.txt', 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open('settings.txt', 'w+')
            if len(list_strings) >= 4:
                list_strings[3] = 'secretkey=' + self.lineEdit_5.text()
            else:
                list_strings.append('apikey=')
                list_strings.append('secretkey=' + self.lineEdit_5.text())
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')
            file.close()

        if self.lineEdit_6.text() != self.bitcoinkey:
            file = open('settings.txt', 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open('settings.txt', 'w+')
            if len(list_strings) >= 5:
                list_strings[4] = 'bitcoin=' + self.lineEdit_6.text()
            else:
                if len(list_strings) == 3:
                    list_strings.append('apikey=')
                list_strings.append('secretkey=')
                list_strings.append('bitcoin=' + self.lineEdit_6.text())
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')
            file.close()

        con.commit()
        con.close()
