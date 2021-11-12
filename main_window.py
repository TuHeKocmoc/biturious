import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5 import QtWidgets, QtGui
from parse import parse
from menu_script import Menu
from PyQt5.QtCore import Qt, QThread
from miner import Implementation
from main_win import Ui_MainWindow as Ui_Main
import cgitb

cgitb.enable(format='text')


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