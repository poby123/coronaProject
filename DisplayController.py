'''
    Last Edit Date : 2020 09 30
    Author : 이원주
    Project Name : 체온측정 스캐너
'''

import sys
from multiprocessing import Process, Queue
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from UI import MenuDisplay, TempInfoDisplay, MsgDisplay, AdminDeleteDisplay, AdminAddDisplay # windows for display
import DataController # to communicate with server
import RasberryController # to communicate with rasberry pi board

class DisplayController():
    #python constructor
    def __init__(self, requestQ, dto, interrupt):

        # GUI program application
        self.app = QtWidgets.QApplication(sys.argv)

        # windows dictionary to manage windows
        self.windows = {}
        self.windowsStack = ['menuWindow']

        # background process running flag for interrupting or not for a adminDelete_cancel (at 2020.09.30)
        self.isRunning = False

        #DTO, requestQ, interrupt
        self.requestQ = requestQ #to send request to background process
        self.dto = dto # to get data from bacground process
        self.interrupt = interrupt # for send interrupt signal from app to bacground process

        #initialize menu window
        MenuWindow = QtWidgets.QMainWindow()
        MenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler, {"menu_name":['사용자 메뉴', '관리자 메뉴'], "event_name":['userMenu', 'adminMenu']})
        MenuWindowUI.setupUi(MenuWindow)
        MenuWindow.show()

        #initialize admin menu window
        AdminMenuWindow = QtWidgets.QMainWindow()
        AdminMenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler, {"menu_name":['추가', '삭제'], "event_name":['adminAdd', 'adminDelete']})
        AdminMenuWindowUI.setupUi(AdminMenuWindow)
        AdminMenuWindow.hide()

        #initialize tempInfo window
        TempInfoWindow = QtWidgets.QMainWindow()
        TempInfoWindowUI = TempInfoDisplay.Ui_TempInfoWindow(37.5, self.menuEventHandler)
        TempInfoWindowUI.setupUi(TempInfoWindow)
        TempInfoWindow.hide()

        #append windows
        self.windows['menuWindow'] = {"window" : MenuWindow, "ui" : MenuWindowUI}
        self.windows['adminMenuWindow'] = {"window":AdminMenuWindow, "ui":AdminMenuWindowUI}
        self.windows['tempInfoWindow'] = {"window":TempInfoWindow, "ui":TempInfoWindowUI}

        #thread for get DTO from background process. A target function is "self.isChanged".
        self.thread = threading.Thread(target=self.isChanged, daemon=True)
        self.thread.start()

        #to set message at tempInfowindow, initializing self.name, uid, temp
        self.init()

    # Thread target function that is used for get DTO from background process
    def isChanged(self):
        while(True):
            time.sleep(0.5)
            if(self.dto.qsize()>0):
                print('is changed')
                item = self.dto.get() # get dto item from background process

                # NFC_NAME type
                if(item['type'] == 'NFC_NAME'):
                    if(item['uid'] != None):
                        self.uid = item['uid']
                    if(item['name'] != None):
                        self.name = item['name']
                        self.windows['tempInfoWindow']['ui'].setName(self.name)
                        self.windows['tempInfoWindow']['ui'].setStatus('체온 측정 중입니다...')
                        self.menuEventHandler('tempInfo')
                    else:
                        self.windows['tempInfoWindow']['ui'].setName('등록되지 않은 카드입니다')
                        time.sleep(1.5) # delay time for display message
                        self.init()
                        self.menuEventHandler('userMenu')
                
                # TEMP type
                elif(item['type'] == 'TEMP'):
                    if(item['temp'] != None):
                        self.temp = item['temp']
                        self.windows['tempInfoWindow']['ui'].setStatus(self.temp)
                    else :
                        self.windows['tempInfoWindow']['ui'].setStatus('오류가 발생했습니다')
                    time.sleep(1.5)
                    self.init()
                    self.menuEventHandler('userMenu') #back to userMenu

                # NFC_ID type
                elif(item['type'] == 'NFC_ID'):
                    self.isRunning = False
                    if(item['uid'] != None):
                        self.windows['adminAddWindow']['ui'].setUID(item['uid'])
                    else :
                        self.windows['adminAddWindow']['ui'].setStatus('NFC 카드를 인식하지 못했습니다')

                # INTERRUPT type
                elif(item['type'] == 'INTERRUPT'):
                    print('interrupted is ouccured')
                
             
    #select window to show for window transistion
    def selectWindow(self, new):
        before = self.windowsStack[-1]
        if(new != before):
            self.windows[before]['window'].hide()
        self.windowsStack.append(new)
        self.windows[new]['window'].show()

    #Handle events from whole windows
    def menuEventHandler(self, arg, others=None):
        self.requestQ.put(arg) #put request at requestQ to request to background process

        # Handle event that user selected userMenu
        if(arg == 'userMenu'):
            self.init()
            self.selectWindow('tempInfoWindow')
        
        # Handle event that user selected adminMenu
        elif(arg == 'adminMenu'):
            self.init()
            self.selectWindow('adminMenuWindow')

        # Hadle event that user selected adminAdd in adminMenu
        elif(arg == 'adminAdd'):
            # Initializing adminAddWindow
            adminAddWindow = QtWidgets.QMainWindow()
            ui = AdminAddDisplay.Ui_MainWindow(self.menuEventHandler)
            ui.setupUi(adminAddWindow)
            ui.setStatus('사용자 추가 페이지입니다\n')
            ui.setUID('NFC 카드를 태그에 대주세요')
            adminAddWindow.show()

            # Append adminAddwindow to self.windows
            self.windows['adminAddWindow'] = {'window':adminAddWindow, 'ui':ui}
            self.isRunning = True

        # Handle user "add" event from adminAddWindow
        elif(arg == 'adminAdd_add'):
            print('add event')
            if(others['uid'] != '' and others['name'] != ''):
                result = DataController.addUser(others['uid'], others['name'], others['belong'])
                print('adminAdd_add result : ', result)
                if(result == True):
                    self.windows['adminAddWindow']['ui'].setStatus('추가에 성공했습니다.')
                else:
                    self.windows['adminAddWindow']['ui'].setStatus('저장에 실패했습니다.\nNFC ID가 같은 사람이 있는지 \n"삭제" 탭에서 확인해주세요')
            else:
                self.windows['adminAddWindow']['ui'].setStatus('NFC ID와 이름은 필수항목입니다.')
 
        # Handle "cancel" event from adminAddWindow
        elif(arg == 'adminAdd_cancel'):
            print('adminAdd_Cancel is clicked')
            if(self.isRunning):
                self.interrupt.put('admdinAdd_cancel')
            self.windows['adminAddWindow']['window'].hide()
        
        # Hadle event that user selected adminDelete in adminMenu
        elif(arg == 'adminDelete'):
            data = DataController.getUserData()
            print(data)
            adminDeleteWindow = QtWidgets.QMainWindow()
            ui = AdminDeleteDisplay.Ui_MainWindow(data, self.menuEventHandler)
            ui.setupUi(adminDeleteWindow)
            adminDeleteWindow.show()
            self.windows['adminDeleteWindow'] = {'window':adminDeleteWindow, 'ui':ui}
        
        # Handle "delete" event from adminDeleteWindow
        elif(arg == 'adminDelete_delete'):
            print(others)
            if(len(others) > 0):
                result = DataController.deleteUser(others)
                if(result):
                    print('삭제에 성공했습니다')
                    data = DataController.getUserData()
                    self.windows['adminDeleteWindow']['ui'].setData(data)
                    self.windows['adminDeleteWindow']['ui'].setupUi(self.windows['adminDeleteWindow']['window'])
                else:
                    print('삭제에 실패했습니다')

        # Handle "cancel" event from adminDeleteWindow
        elif(arg == 'adminDelete_cancel'):
            self.windows['adminDeleteWindow']['window'].hide()


    #Initializing
    def init(self):
        self.windows['tempInfoWindow']['ui'].setName('확인 중... NFC카드를 대주세요')
        self.windows['tempInfoWindow']['ui'].setStatus('환영합니다')
        self.name = ''
        self.uid = ''
        self.temp = ''
    
    def clear(self):
        while(self.requestQ.qsize() > 0):
            self.requestQ.get()
        while(self.dto.qsize() > 0):
            self.dto.get()

def Handler(requestQ, dto, interrupt):
    while(True):
        time.sleep(0.5)
        if(requestQ.qsize()>0):
            item = requestQ.get()
            if(item == 'userMenu'):
                dto.put(RasberryController.getNameByNFC())
            elif(item == 'tempInfo'):
                dto.put(RasberryController.getTemp())
            elif(item == 'adminAdd'):
                print('adminAdd_add is called in Handler')
                dto.put(RasberryController.getNFCId(interrupt))
            


if __name__ == "__main__":
    requestQ = Queue()
    dto = Queue()
    interrupt = Queue()

    displayController = DisplayController(requestQ, dto, interrupt) #insert requestQ, dto, interrupt as args of displaycontroller
    app = displayController.app

    handler = Process(target=Handler, args=(requestQ,dto,interrupt,), daemon=True) #set as daemon process
    handler.start() #background process start

    sys.exit(app.exec())