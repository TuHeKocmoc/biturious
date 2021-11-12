import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5 import QtWidgets
from parse import parse
from menu_script import Menu
from PyQt5.QtCore import Qt
from miner import Implementation
from main_win import Ui_MainWindow as Ui_Main


class MainWindow(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plainTextEdit_3.insertPlainText(parse())
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
        else:
            self.label_2.setText('Не работает')
            self.label_2.move(83, 130)
            self.label_2.resize(135, 25)

    def rollup(self):
        self.showMinimized()

    def my_close(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    #import threading


    # init threads
    #def pipka():
        #for i in range(10):
            #print('1')


    #e1 = threading.Event()
    #e2 = threading.Event()

    #t1 = threading.Thread(target=ex.initUI)
    #t2 = threading.Thread(target=Implementation().mining_forever)

    #t1.start()
    #t2.start()

    #e1.set()  # initiate the first event

    # join threads to the main thread
    #t1.join()
    #t2.join()

    sys.exit(app.exec())
