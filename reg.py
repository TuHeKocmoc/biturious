import sys
import sqlite3
import re
import os
import smtplib
import random
import uuid
import hashlib

from email.mime.text import MIMEText
from requests import get
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from regui import Ui_MainWindow as Ui_Reg
from activateui import Ui_MainWindow as Ui_Activate

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def check_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email)


def check_acc(username, email):
    con = sqlite3.connect("auth.db")
    cur = con.cursor()
    true_email = cur.execute("""SELECT email FROM users 
                    WHERE login = ? """, (username, )).fetchall()
    return email == true_email[0][0]


def exit_app():
    sys.exit(app.exec())


def hash_password(password):
    salt = uuid.uuid4().hex
    os.environ['SALT'] = 'bK4-LbL-fT7-2WB'
    res = hashlib.sha512(os.getenv('SALT').encode() + salt.encode() + password.encode()).hexdigest() + ':' + salt
    os.environ.clear()
    return res


def get_ip():
    ip = get('https://api.ipify.org').text
    return ip


def send_code(email):
    code = random.randrange(100000, 999999)
    mail_user = 'bot@biturious.space'
    os.environ['MAIL_PASSWORD'] = 'XBG-dqP-3ES-Dbg'
    mail_pwd = os.getenv('MAIL_PASSWORD', '123456')
    content = """Пожалуйста, введите код в программу для завершения регистрации или восстановления пароля.
    Никому не сообщайте ваш код.
    Ваш код: """ + str(code)
    message = MIMEText(content, 'html')
    message['Subject'] = 'Личный код Biturious'
    message['From'] = mail_user
    message['To'] = email
    mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    mail.login(mail_user, mail_pwd)
    if not check_email(email):
        return False
    to = email
    mail.sendmail(mail_user, to, message.as_string())
    mail.quit()
    os.environ.clear()
    return code


class Reg(QMainWindow, Ui_Reg):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.main = args[0]
        self.lineEdit_5.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_4.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_4.setText(args[0].lineEdit.text())
        self.lineEdit_5.setText(args[0].lineEdit_2.text())
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton_4.clicked.connect(self.reg)
        self.pushButton_5.clicked.connect(exit_app)

    def reg(self):
        self.label_5.setText('')
        self.label_6.setText('')
        self.label_7.setText('')

        login = self.lineEdit_4.text()
        password = self.lineEdit_5.text()
        email = self.lineEdit_2.text()

        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        logins = cur.execute("SELECT login FROM users").fetchall()
        emails = cur.execute("SELECT email FROM users").fetchall()

        res2 = []
        res = []

        for i in logins:
            for j in i:
                res.append(j)
        for i in emails:
            for j in i:
                res2.append(j)

        if login in res:
            self.label_5.setText('Данный логин уже используется')
            con.close()
            return 0
        elif not login:
            self.label_5.setText('Обязательно для заполнения')
            con.close()
            return 0
        elif not email:
            self.label_7.setText('Обязательно для заполнения')
            con.close()
            return 0
        elif email in res2:
            self.label_7.setText('Данная почта уже используется')
            con.close()
            return 0
        elif not check_email(email):
            self.label_7.setText('Данная почта не существует')
            con.close()
            return 0
        elif not password:
            self.label_6.setText('Обязательно для заполнения')
            con.close()
            return 0
        elif len(password) < 6:
            self.label_6.setText('Слабый пароль, используйте другой')
            con.close()
            return 0
        con.close()
        self.close()
        self.next = Activate(self, self.main)
        self.next.show()


class Activate(QMainWindow, Ui_Activate):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.main = args[1]
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.activate)
        self.pushButton_4.clicked.connect(exit_app)
        self.email = args[0].lineEdit_2.text()
        self.password = args[0].lineEdit_5.text()
        self.login = args[0].lineEdit_4.text()
        self.true_code = send_code(self.email)

    def activate(self):
        self.label_2.setText('')

        code = self.lineEdit.text()

        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        if int(code) != int(self.true_code):
            self.label_2.setText('Введен неверный код')
            con.close()
            return 0

        cur.execute("INSERT INTO users(login, password, email, last_ip, reg_ip, balance, allow_pass_change) "
                    "VALUES(?, ?, ?, ?, ?, ?, ?)",
                    (self.login, hash_password(self.password), self.email, get_ip(), get_ip(), 0.0, True))
        con.commit()
        con.close()
        self.close()
        self.main.show()
