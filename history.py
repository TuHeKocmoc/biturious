import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from payments import Ui_MainWindow as Ui_Payments

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class History(QMainWindow, Ui_Payments):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        file = open('settings.txt', 'r')
        logpass = file.readlines()
        login = logpass[0].strip()
        self.login = login[login.find('=') + 1:]
        file.close()
        self.main = args[0]
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton_4.clicked.connect(self.exit_app)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        con = sqlite3.connect("auth.db")
        cur = con.cursor()
        user_payments = cur.execute("""SELECT * FROM payments
                            WHERE getter = ? """, (self.login,)).fetchall()
        con.close()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        headers = 'ID Операции;Логин;0 - продажа, 1 - покупка;Время;Количество'.split(';')
        self.tableWidget.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(user_payments):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def exit_app(self):
        self.main.show()
        self.close()