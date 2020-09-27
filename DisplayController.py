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

        #windows dictionary
        self.windows = {}
        self.windowsStack = ['menuWindow']

        #DTO
        self.dto = {"uid":0, "name":None, "temp":0}

        #init menu window
        MenuWindow = QtWidgets.QMainWindow()
        MenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler)
        MenuWindowUI.setupUi(MenuWindow)
        MenuWindow.show()

        #init tempInfo window
        TempInfoWindow = QtWidgets.QMainWindow()
        TempInfoWindowUI = TempInfoDisplay.Ui_TempInfoWindow(37.5, self.menuEventHandler)
        TempInfoWindowUI.setupUi(TempInfoWindow)
        TempInfoWindowUI.setName('확인 중... NFC카드를 대주세요')
        TempInfoWindow.hide()

        #init msg window
        MsgWindow = QtWidgets.QMainWindow()
        MsgWindowUI = MsgDisplay.Ui_MsgWindow('', self.menuEventHandler)
        MsgWindowUI.setupUi(MsgWindow)
        MsgWindow.hide()

        #append windows
        self.windows['menuWindow'] = {"window" : MenuWindow, "ui" : MenuWindowUI}
        self.windows['msgWindow'] = {"window":MsgWindow, "ui":MsgWindowUI}
        self.windows['tempInfoWindow'] = {"window":TempInfoWindow, "ui":TempInfoWindowUI}

    def __del__(self):
        if(self.NFCThread != None):
            self.NFCThread.join()
        if(self.tempThread != None):
            self.tempThread.join()

    def selectWindow(self, new):
            before = self.windowsStack[-1]
            self.windows[before]['window'].hide()
            self.windowsStack.append(new)
            self.windows[new]['window'].show()

    def menuEventHandler(self, arg, msg = None):
        print(arg)
        if(arg == 'userMenu'):
            self.NFCThread = RasberryController.RasberryController(self.dto, self.NFCThreadEvent, 'NFC')
            self.menuEventHandler('tempInfo')
            self.NFCThread.start()

        elif(arg=='adminMenu'):
            pass
        elif(arg=='tempInfo'):
            self.selectWindow('tempInfoWindow')
            self.tempThread = RasberryController.RasberryController(self.dto, self.TempThreadEvent, 'temp')
            self.tempThread.start()
            
        elif(arg=='backwardAtUserMenu'):
            self.selectWindow('menuWindow')
            
    def NFCThreadEvent(self):
        if(self.dto['name'] != None):
            self.windows['tempInfoWindow']["ui"].setName(self.dto['name'])
            self.windows['tempInfoWindow']["ui"].setStatus('체온측정 중입니다.')

    def TempThreadEvent(self):
        # self.NFCThread.join()
        if(self.dto['name'] == None):
            self.dto['temp'] = '등록되어 있지 않은 NFC카드입니다'
        self.windows['tempInfoWindow']["ui"].setStatus(self.dto['temp'])
        time.sleep(1.5)
        for i in range(0,4):
            time.sleep(1)
            self.windows['tempInfoWindow']["ui"].setStatus(f"{3-i} 초후에 돌아갑니다")
        self.backToUserMenu()

    def initDTO(self):
        self.dto['uid'] = 0
        self.dto['name'] = None
        self.dto['temp'] = 0

    def backToUserMenu(self):
        #init
        self.windows['tempInfoWindow']['ui'].setName('확인 중... NFC카드를 대주세요')
        self.windows['tempInfoWindow']['ui'].setStatus('')
        self.initDTO()
        self.menuEventHandler('userMenu')


if __name__ == "__main__":
    displayController = DisplayController()
    app = displayController.app
    sys.exit(app.exec())