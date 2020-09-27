from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import threading
import time
#user defined module
from UI import MenuDisplay, TempInfoDisplay, MsgDisplay
import RasberryController
class DisplayController():
    def __init__(self):
        # application
        self.app = QtWidgets.QApplication(sys.argv)

        #windows stack list
        self.windows = []

        #DTO
        self.dto = {"uid":0, "name":None, "temp":0}

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
        self.windows.append({"window":MsgWindow, "ui":MsgWindowUI})

    def makeTempInfoDisplay(self):
        TempInfoWindow = QtWidgets.QMainWindow()
        TempInfoWindowUI = TempInfoDisplay.Ui_TempInfoWindow(37.5, self.menuEventHandler)
        TempInfoWindowUI.setupUi(TempInfoWindow)
        TempInfoWindow.show()
        self.windows.append({"window":TempInfoWindow, "ui":TempInfoWindowUI})

    def menuEventHandler(self, arg, msg = None):
        print(arg)
        if(arg == 'userMenu'):
            self.displayTransition('forward')
            self.makeMsgDisplay('환영합니다! NFC카드를 대주세요!')
            #rasberry controller
            self.NFCThread = RasberryController.RasberryController(self.dto, self.NFCThreadEvent, 'NFC')
            self.menuEventHandler('tempInfo')
            self.NFCThread.start()

        elif(arg == 'msg'):
            print('it is called')
            self.displayTransition('forward')
            self.makeMsgDisplay(msg)

        elif(arg=='adminMenu'):
            pass
        elif(arg=='tempInfo'):
            self.displayTransition('forward')
            self.makeTempInfoDisplay()
            self.tempThread = RasberryController.RasberryController(self.dto, self.TempThreadEvent, 'temp')
            self.tempThread.start()
            
        elif(arg=='backward'):
            if(len(self.windows) > 1):
                self.windows.pop()
                self.displayTransition('backward')

    def displayTransition(self, cmd):
        if(cmd == 'forward'):
            self.windows[-1]["window"].hide()
        elif(cmd == 'backward'):
            self.windows[-1]["window"].show()

    def NFCThreadEvent(self):
        if(self.dto['name'] != None):
            self.windows[-1]["ui"].setName(self.dto['name'])
            self.windows[-1]["ui"].setStatus('체온측정 중입니다.')

    def TempThreadEvent(self):
        self.NFCThread.join()
        if(self.dto['name'] == None):
            self.dto['temp'] = '등록되어 있지 않은 NFC카드입니다'
        self.windows[-1]["ui"].setStatus(self.dto['temp'])

         
if __name__ == "__main__":
    displayController = DisplayController()
    app = displayController.app
    sys.exit(app.exec())