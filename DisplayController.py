# --- default module
import sys
from multiprocessing import Process, Queue
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
    def __init__(self, requestQ, dto):
        # GUI program application
        self.app = QtWidgets.QApplication(sys.argv)

        #windows dictionary
        self.windows = {}
        self.windowsStack = ['menuWindow']

        #DTO, requestQ
        self.requestQ = requestQ
        self.dto = dto

        #status
        self.name = ''
        self.uid = ''
        self.temp = ''

        #interrupt flag
        self.interrupt = False

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
        TempInfoWindowUI.setStatus('')
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

        #thread
        self.thread = threading.Thread(target=self.isChanged, daemon=True)
        self.thread.start()

    def isChanged(self):
        while(True):
            time.sleep(0.5)
            if(self.dto.qsize()>0):
                print('is changed')
                item = self.dto.get()
                if(item['type'] == 'NFC'):
                    if(item['uid'] != None):
                        self.uid = item['uid']
                    if(item['name'] != None):
                        self.name = item['name']
                        self.windows['tempInfoWindow']['ui'].setName(self.name)
                        self.menuEventHandler('tempInfo')
                    else:
                        self.windows['tempInfoWindow']['ui'].setName('등록되지 않은 카드입니다')
                        time.sleep(1.5)
                        self.init()
                        self.menuEventHandler('userMenu')
                            
                    # print(self.name, self.uid, self.temp)
                elif(item['type'] == 'TEMP'):
                    if(item['temp'] != None):
                        self.temp = item['temp']
                        self.windows['tempInfoWindow']['ui'].setStatus(self.temp)
                    else :
                        self.windows['tempInfoWindow']['ui'].setStatus('오류가 발생했습니다')
                    time.sleep(1.5)
                    self.init()
                    self.menuEventHandler('userMenu')
                

                
    #select window to show for window transistion
    def selectWindow(self, new):
        before = self.windowsStack[-1]
        if(new != before):
            self.windows[before]['window'].hide()
        self.windowsStack.append(new)
        self.windows[new]['window'].show()

    #Handle events at windows
    def menuEventHandler(self, arg):
        #put request
        self.requestQ.put(arg)

        if(arg == 'userMenu'):
            self.init()
            self.selectWindow('tempInfoWindow')

        elif(arg=='adminMenu'):
            pass
        elif(arg=='tempInfo'):
            pass
            # self.selectWindow('tempInfoWindow')
            
        elif(arg=='backwardAtUserMenu'):
            self.selectWindow('menuWindow') #return to menuWindow
            self.init() #DTO, windows initializing
            self.clear()

    #Initializing
    def init(self):
        self.windows['tempInfoWindow']['ui'].setName('확인 중... NFC카드를 대주세요')
        self.windows['tempInfoWindow']['ui'].setStatus('')
        self.name = ''
        self.uid = ''
        self.temp = ''
    
    def clear(self):
        while(self.requestQ.qsize() > 0):
            self.requestQ.get()
        while(self.dto.qsize() > 0):
            self.dto.get()


def Handler(requestQ, dto):
    while(True):
        time.sleep(0.5)
        if(requestQ.qsize()>0):
            item = requestQ.get()
            if(item == 'userMenu'):
                dto.put(RasberryController.getNFC())
            elif(item == 'tempInfo'):
                dto.put(RasberryController.getTemp())
            


if __name__ == "__main__":
    requestQ = Queue()
    dto = Queue()
    
    displayController = DisplayController(requestQ, dto)
    app = displayController.app
    handler = Process(target=Handler, args=(requestQ,dto), daemon=True)
    handler.start()

    sys.exit(app.exec())