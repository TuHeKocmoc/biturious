import sys
import sqlite3
import re
import os
import random
import hashlib
from reg import Reg
from forgot import Forgot

from requests import get
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from mainui import Ui_Login

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def check_acc(username, email):
    con = sqlite3.connect("auth.db")
    cur = con.cursor()
    true_email = cur.execute("""SELECT email FROM users 
                    WHERE login = ? """, (username, )).fetchall()
    return email == true_email[0][0]


def exit_app():
    sys.exit(app.exec())


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    os.environ['SALT'] = 'bK4-LbL-fT7-2WB'
    res = password == hashlib.sha512(os.getenv('SALT').encode() + salt.encode() + user_password.encode()).hexdigest()
    os.environ.clear()
    return res


def get_ip():
    ip = get('https://api.ipify.org').text
    return ip


class Login(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

        self.pushButton.clicked.connect(self.authorize)
        self.pushButton_3.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.forgot_password)
        self.pushButton_4.clicked.connect(exit_app)

    def authorize(self):
        self.label_2.setText('Пожалуйста, представьтесь')
        self.label_2.setStyleSheet('QLabel { color: grey }')
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        con = sqlite3.connect("auth.db")
        cur = con.cursor()
        logins = cur.execute("SELECT login FROM users").fetchall()
        res = []
        for i in logins:
            for j in i:
                res.append(j)
        if not login:
            self.label_2.setText('Вы не ввели логин')
            self.label_2.setStyleSheet('QLabel { color: red }')
            return 0
        elif not password:
            self.label_2.setText('Вы не ввели пароль')
            self.label_2.setStyleSheet('QLabel { color: red }')
            return 0
        elif login not in res:
            self.label_2.setText('Неправильный логин или пароль')
            self.label_2.setStyleSheet('QLabel { color: red }')
            return 0
        else:
            true_password = cur.execute("""SELECT password FROM users 
                    WHERE login = ? """, (login, )).fetchall()
            if not check_password(true_password[0][0], password):
                self.label_2.setText('Неправильный логин или пароль')
                self.label_2.setStyleSheet('QLabel { color: red }')
                return 0
        self.label_2.setText('OK, ' + login)
        self.label_2.setStyleSheet('QLabel { color: green }')
        cur.execute("""UPDATE users 
                SET last_ip = ? 
                WHERE login = ?""", (get_ip(), login))
        con.commit()
        con.close()

    def reg(self):
        self.close()
        self.register = Reg(self)
        self.register.show()

    def forgot_password(self):
        self.close()
        self.forgot = Forgot(self)
        self.forgot.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    exit_app()
