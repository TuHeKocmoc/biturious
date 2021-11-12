# -*- coding: utf-8 -*-

import sys
import re
import datetime
import uuid
import hashlib
import sqlite3
import string
import os
import pathlib

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from settingsui import Ui_MainWindow as Ui_Settings


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


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Settings(QMainWindow, Ui_Settings):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        con = sqlite3.connect("auth.db")
        cur = con.cursor()
        file = open('settings.txt', 'r')
        logpass = file.readlines()
        login = logpass[0].strip()
        password = logpass[1].strip()
        self.login = login[login.find('=') + 1:]
        self.password = password[password.find('=') + 1:]
        file.close()
        self.main = args[0]
        self.lineEdit.setText(self.login)
        email = cur.execute("""SELECT email FROM users 
                            WHERE login = ? """, (self.login,)).fetchall()
        self.email = email[0][0]
        self.lineEdit_2.setText(self.email)
        self.lineEdit_3.setText(self.password)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.exit_app)
        self.pushButton_2.clicked.connect(self.check)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_3.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_4.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_5.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_6.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.path = str(pathlib.Path(__file__).parent.resolve()) + '\settings.txt'
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
        self.label_2.setText('')
        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        if self.lineEdit_2.text() != self.email:
            self.email = self.lineEdit_2.text()
            if not self.email:
                self.label_2.setText('Вы не ввели почту!')
                con.close()
                return 0
            elif not check_email(self.email):
                self.label_2.setText('Вы ввели неверную почту')
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
                self.label_2.setText('Вы не ввели пароль!')
                con.close()
                return 0

            elif not check_pass(self.password):
                self.label_2.setText('Пароль содержит запрещенные символы')
                con.close()
                return 0

            true_password = cur.execute("""SELECT password FROM users 
                             WHERE login = ? """, (self.login,)).fetchall()

            cur.execute("INSERT INTO password_changes(user, time, old_password, new_password) VALUES(?, ?, ?, ?)",
                        (self.login, datetime.datetime.now(), true_password[0][0], hash_password(self.password)))

            cur.execute("""UPDATE users 
                            SET password = ? 
                            WHERE email = ?""", (hash_password(self.password), self.login))

            file = open(self.path, 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open(self.path, 'w+')
            list_strings[1] = 'password=' + self.password
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')

        if self.lineEdit_4.text() != self.apikey:
            file = open(self.path, 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open(self.path, 'w+')
            list_strings[2] = 'apikey=' + self.lineEdit_4.text()
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')
            file.close()

        if self.lineEdit_5.text() != self.secretkey:
            file = open(self.path, 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open(self.path, 'w+')
            if len(list_strings) >= 4:
                list_strings[3] = 'secretkey=' + self.lineEdit_5.text()
            else:
                print('ok')
                list_strings.append('apikey=')
                list_strings.append('secretkey=' + self.lineEdit_5.text())
            for i in list_strings:
                tmp = i.strip()
                if tmp:
                    file.write(tmp)
                    file.write('\n')
            file.close()

        if self.lineEdit_6.text() != self.bitcoinkey:
            file = open(self.path, 'r+')
            text = file.read()
            list_strings = text.split('\n')
            file.close()
            file = open(self.path, 'w+')
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
        self.exit_app()

    def exit_app(self):
        self.close()
        self.main.show()
