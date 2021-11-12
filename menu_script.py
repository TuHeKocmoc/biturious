from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from Chart import Graph
from support import Help
from stock import Stock
from support_stock import Help_Stock
from gpu import GPU
from menu_dis import Ui_MainWindow as Ui_Menu

CLASSES = {
    'График курса Bitcoin': Graph,
    'Помощь': Help,
    'Продажа и покупка Bitcoin': Stock,
    'Помощь в покупке и продаже Bitcoin': Help_Stock,
    'Лучшие видеокарты': GPU
}


class Menu(QMainWindow, Ui_Menu):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.back_in_main = args
        self.initUI()

    def initUI(self):
        self.move(500, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.options)
        self.pushButton_2.clicked.connect(self.options)
        self.pushButton_3.clicked.connect(self.options)
        self.pushButton_4.clicked.connect(self.options)
        self.pushButton_5.clicked.connect(self.options)
        self.pushButton_6.clicked.connect(self.options)
        self.pushButton_7.clicked.connect(self.options)
        self.pushButton_8.clicked.connect(self.options)
        self.pushButton_9.clicked.connect(self.options)

    def options(self):
        option = self.sender().text()
        if option != '←':
            self.second_form = CLASSES[option](self)
            self.second_form.show()
        else:
            self.back_in_main[0].show()
        self.close()
