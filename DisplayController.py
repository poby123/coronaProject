from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from UI import MenuDisplay, TempInfoDisplay, MsgDisplay

class DisplayController():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.windows = []

        #init menu window
        self.MenuWindow = QtWidgets.QMainWindow()
        self.MenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler)
        self.MenuWindowUI.setupUi(self.MenuWindow)
        self.MenuWindow.show()

        #append menu window
        self.windows.append({"window" : self.MenuWindow, "ui" : self.MenuWindowUI})

    def makeMsgDisplay(self, msg):
        MsgWindow = QtWidgets.QMainWindow()
        MsgWindowUI = MsgDisplay.Ui_MsgWindow(msg, self.menuEventHandler)
        MsgWindowUI.setupUi(MsgWindow)
        MsgWindow.show()
        self.windows.append({"window" : MsgWindow, "ui":MsgWindowUI})

    def menuEventHandler(self, arg):
        print(arg)
        if(arg == 'userMenu'):
            self.displayTransition('forward')
            self.makeMsgDisplay('환영합니다! NFC카드를 대주세요!')
        elif(arg=='adminMenu'):
            pass
        elif(arg=='backward'):
            if(len(self.windows) > 1):
                self.windows.pop()
                self.displayTransition('backward')

    def displayTransition(self, cmd):
        if(cmd == 'forward'):
            self.windows[-1]["window"].hide()
        elif(cmd == 'backward'):
            self.windows[-1]["window"].show()
         

if __name__ == "__main__":
    diplayController = DisplayController()
    sys.exit(diplayController.app.exec())