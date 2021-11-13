from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from parse_gpu import parse


class GPU(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.back_in_menu = args
        self.initUI()

    def initUI(self):
        self.move(500, 150)
        self.resize(800, 600)
        self.setStyleSheet('background-color: black')
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.pushButton = QPushButton(self)
        self.pushButton.move(10, 10)
        self.pushButton.resize(51, 41)
        self.pushButton.setStyleSheet('background-color: black; color: white; font: 20pt "Ubuntu";')
        self.pushButton.setText('←')

        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.setStyleSheet('background-color: rgb(46, 52, 54); color: white; font: 20pt "Ubuntu"')
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.move(50, 91)
        self.plainTextEdit.resize(700, 450)
        text = parse()
        text = ''.join([data + '\n' + ' ' + '\n' for data in text])
        self.plainTextEdit.setPlainText(text)

        self.label = QLabel(self)
        self.label.move(125, 20)
        self.label.resize(620, 45)
        self.label.setStyleSheet('color: white; font: 23pt "Ubuntu"')
        self.label.setText('Лучшие видеокарты для майнинга')

        self.pushButton.clicked.connect(self.exit)
        self.show()

    def exit(self):
        self.back_in_menu[0].show()
        self.close()
