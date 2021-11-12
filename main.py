import sys
import sqlite3
import re
import os
import random
import hashlib
import pathlib
import time
from reg import Reg
from forgot import Forgot

from requests import get
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from mainui import Ui_Login
from main_window import MainWindow

import os
import shutil
import ctypes

if sys.platform == 'win32' or sys.platform == 'cygwin':
    from ctypes import wintypes

    try:
        import winreg
    except ImportError:
        import _winreg as winreg

user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

FONTS_REG_PATH = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'

HWND_BROADCAST = 0xFFFF
SMTO_ABORTIFHUNG = 0x0002
WM_FONTCHANGE = 0x001D
GFRI_DESCRIPTION = 1
GFRI_ISTRUETYPE = 3

if not hasattr(wintypes, 'LPDWORD'):
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

user32.SendMessageTimeoutW.restype = wintypes.LPVOID
user32.SendMessageTimeoutW.argtypes = (
    wintypes.HWND,  # hWnd
    wintypes.UINT,  # Msg
    wintypes.LPVOID,  # wParam
    wintypes.LPVOID,  # lParam
    wintypes.UINT,  # fuFlags
    wintypes.UINT,  # uTimeout
    wintypes.LPVOID)  # lpdwResult

gdi32.AddFontResourceW.argtypes = (
    wintypes.LPCWSTR,)  # lpszFilename

gdi32.GetFontResourceInfoW.argtypes = (
    wintypes.LPCWSTR,  # lpszFilename
    wintypes.LPDWORD,  # cbBuffer
    wintypes.LPVOID,  # lpBuffer
    wintypes.DWORD)  # dwQueryType


def install_font(src_path):
    # copy the font to the Windows Fonts folder
    dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                            os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    # load the font in the current session
    if not gdi32.AddFontResourceW(dst_path):
        os.remove(dst_path)
        raise WindowsError('AddFontResource failed to load "%s"' % src_path)
    # notify running programs
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0,
                               SMTO_ABORTIFHUNG, 1000, None)
    # store the fontname/filename in the registry
    filename = os.path.basename(dst_path)
    fontname = os.path.splitext(filename)[0]
    # try to get the font's real name
    cb = wintypes.DWORD()
    if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                  GFRI_DESCRIPTION):
        buf = (ctypes.c_wchar * cb.value)()
        if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                      GFRI_DESCRIPTION):
            fontname = buf.value
    is_truetype = wintypes.BOOL()
    cb.value = ctypes.sizeof(is_truetype)
    gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), ctypes.byref(is_truetype), GFRI_ISTRUETYPE)
    if is_truetype:
        fontname += ' (TrueType)'
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0,
                        winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)


if sys.platform == 'win32' or sys.platform == 'cygwin':
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin:
        install_font('font.ttf')

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def check_acc(username, email):
    con = sqlite3.connect("auth.db")
    cur = con.cursor()
    true_email = cur.execute("""SELECT email FROM users 
                    WHERE login = ? """, (username,)).fetchall()
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
        self.path = str(pathlib.Path(__file__).parent.resolve()) + '\settings.txt'

        self.pushButton.clicked.connect(self.authorize)
        self.pushButton_3.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.forgot_password)
        self.pushButton_4.clicked.connect(exit_app)
        self.login = ''
        self.password = ''
        if os.path.exists(self.path):
            file = open('settings.txt', 'r')
            logpass = file.readlines()
            login = logpass[0].strip()
            password = logpass[1].strip()
            self.login = login[login.find('=') + 1:]
            self.password = password[password.find('=') + 1:]
            self.lineEdit.setText(self.login)
            self.lineEdit_2.setText(self.password)
            file.close()

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
                    WHERE login = ? """, (login,)).fetchall()
            if not check_password(true_password[0][0], password):
                self.label_2.setText('Неправильный логин или пароль')
                self.label_2.setStyleSheet('QLabel { color: red }')
                return 0
        self.label_2.setText('OK, ' + login)
        self.close()
        self.label_2.setStyleSheet('QLabel { color: green }')
        cur.execute("""UPDATE users 
                SET last_ip = ? 
                WHERE login = ?""", (get_ip(), login))
        con.commit()
        con.close()
        if not os.path.exists(self.path):
            file = open('settings.txt', 'w+')
            file.write('login=' + login)
            file.write('\n')
            file.write('password=' + password)
            file.write('\n')
            file.close()
        self.close()
        self.next = MainWindow()
        self.next.show()

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
