# --- default module
import sys
import threading #threading for thread
import time

# --- installed module from pip
from PyQt5 import QtCore, QtGui, QtWidgets

# --- user defined module ---
# import windows to be displayed
from UI import MenuDisplay, TempInfoDisplay, MsgDisplay

# import Rasberry pi controller to communicate with rasberry pi board
import RasberryController
class DisplayController():

    #python constructor
    def __init__(self):
        # GUI program application
        self.app = QtWidgets.QApplication(sys.argv)

        #windows dictionary
        self.windows = {}
        self.windowsStack = ['menuWindow']

        #flag variable for thread interrupting
        self.interuppt = False

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
        pass

    #select window to show for window transistion
    def selectWindow(self, new):
        before = self.windowsStack[-1]
        self.windows[before]['window'].hide()
        self.windowsStack.append(new)
        self.windows[new]['window'].show()

    #Handle events at windows
    def menuEventHandler(self, arg, msg = None):
        print(arg)
        if(arg == 'userMenu'):
            self.NFCThread = RasberryController.RasberryController(self.dto, self.NFCThreadEvent, 'NFC')
            self.NFCThread.start()
            self.menuEventHandler('tempInfo')

        elif(arg=='adminMenu'):
            pass
        elif(arg=='tempInfo'):
            self.selectWindow('tempInfoWindow')
            self.tempThread = RasberryController.RasberryController(self.dto, self.TempThreadEvent, 'temp')
            self.tempThread.start()
            
        elif(arg=='backwardAtUserMenu'):
            #thread interrupt
            self.interuppt = True
            print(self.NFCThread.is_alive())
            print(self.tempThread.is_alive())
            if(self.NFCThread.is_alive()):
                self.NFCThread.stop() #thread stop
                self.NFCThread.join() #wait until thread is stopped
            if(self.tempThread.is_alive()):
                self.tempThread.stop() #thread stop
                self.tempThread.join() #wait until thread is stopped
            self.selectWindow('menuWindow') #return to menuWindow

            #DTO, windows initializing
            self.init()
            
    #it is called after getting name from NFCThread and when NFC thread is almost finished
    def NFCThreadEvent(self):
        if(self.interuppt == True):
            return
        if(self.dto['name'] != None):
            self.windows['tempInfoWindow']["ui"].setName(self.dto['name'])
            self.windows['tempInfoWindow']["ui"].setStatus('체온측정 중입니다.')

    #it is called after getting temperature data from TempThread and when temp thread is almost finished
    def TempThreadEvent(self):
        #if interrupt signal is true, it makes be stopped.
        if(self.interuppt == True):
            return
        
        #wait until NFCThread is finished.
        self.NFCThread.join()
        if(self.dto['name'] == None):
            self.dto['temp'] = '등록되어 있지 않은 NFC카드입니다'
        print(self.dto)

        #set temperature at tempInfoWindow
        self.windows['tempInfoWindow']["ui"].setStatus(self.dto['temp'])
        
        #time sleep for showing tempInfo window for 1.5 seconds
        time.sleep(1.5)

        #count down from 3 to 0
        for i in range(0,4):
            time.sleep(1)
            self.windows['tempInfoWindow']["ui"].setStatus(f"{3-i} 초후에 돌아갑니다")
            #if interrupt is true in countdown, it makes be stopped
            if(self.interuppt == True):
                return

        #Initialize and move to userMenu window
        self.init()
        self.menuEventHandler('userMenu')

    #Initializing DTO
    def initDTO(self):
        self.dto['uid'] = 0
        self.dto['name'] = None
        self.dto['temp'] = 0

    #Initializing
    def init(self):
        self.windows['tempInfoWindow']['ui'].setName('확인 중... NFC카드를 대주세요')
        self.windows['tempInfoWindow']['ui'].setStatus('')
        self.initDTO()
        self.tempThread.reset() #reset interrupt flag as False
        self.NFCThread.reset() #reset interrupt flag as False
        # self.NFCThread.join()
        # self.tempThread.join()
        self.interuppt = False


if __name__ == "__main__":
    displayController = DisplayController()
    app = displayController.app
    sys.exit(app.exec())