# -*- coding: utf-8 -*-

import sys
import re
import datetime
import uuid
import hashlib

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from settingsui import Ui_MainWindow as Ui_Settings


def check_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email)


def check_acc(username, email):
    con = sqlite3.connect("auth.db")
    cur = con.cursor()
    true_email = cur.execute("""SELECT email FROM users 
                    WHERE login = ? """, (username, )).fetchall()
    return email == true_email[0][0]


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
        self.login = args[1]
        self.email = args[2]
        self.password = args[3]
        self.main = args[0]
        self.lineEdit.setText(args[1])
        self.lineEdit_2.setText(args[2])
        self.lineEdit_3.setText(args[3])
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.exit_app)
        self.pushButton_2.clicked.conenct(self.check)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_3.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

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
                self.lineEdit.setText('Вы ввели невернуюпочту')
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

            elif not check_pass(password1):
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

        con.commit()
        con.close()
        self.exit_app()

    def exit_app(self):
        self.close()
        self.main.show()
