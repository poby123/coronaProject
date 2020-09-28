# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WelcomeDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MsgWindow(object):

    def __init__(self, msg, MenuEventHandler):
        self.msg = msg
        self.MenuEventHandler = MenuEventHandler

    def handleBackClickEvent(self):
        self.MenuEventHandler('backwardAtUserMenu')

    def setupUi(self, MsgWindow):
        MsgWindow.setObjectName("MsgWindow")
        MsgWindow.resize(780, 390)
        self.centralwidget = QtWidgets.QWidget(MsgWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 50, 661, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 50, 659, 249))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.handleBackClickEvent)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 93, 28))
        self.pushButton.setObjectName("pushButton")
        MsgWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MsgWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 26))
        self.menubar.setObjectName("menubar")
        MsgWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MsgWindow)
        self.statusbar.setObjectName("statusbar")
        MsgWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MsgWindow)
        QtCore.QMetaObject.connectSlotsByName(MsgWindow)

    def retranslateUi(self, MsgWindow):
        _translate = QtCore.QCoreApplication.translate
        # MsgWindow.setWindowTitle(_translate("MsgWindow", "Welcome!"))
        self.label.setText(_translate("MsgWindow", self.msg))
        self.pushButton.setText(_translate("WelcomeWindow", "뒤로가기"))

    def setMsg(self, msg):
        self.label.setText(msg)
