# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forgot2ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(747, 582)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(250, 267, 241, 201))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit.setStyleSheet("QLineEdit {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-style: solid;\n"
"    border-width: 3px;\n"
"    border-color: grey;\n"
"    color: white;\n"
"}\n"
"")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-style: solid;\n"
"    border-width: 3px;\n"
"    border-color: grey;\n"
"    color: white;\n"
"}\n"
"")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_3.setStyleSheet("QLineEdit {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-style: solid;\n"
"    border-width: 3px;\n"
"    border-color: grey;\n"
"    color: white;\n"
"}\n"
"")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3, 0, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 60, 751, 85))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: red;")
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(710, 0, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(16)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("color: white")
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "код с почты"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "пароль"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "повторите пароль"))
        self.pushButton.setText(_translate("MainWindow", "Восстановить пароль"))
        self.label.setText(_translate("MainWindow", "Восстановление пароля"))
        self.pushButton_5.setText(_translate("MainWindow", "←"))
