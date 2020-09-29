# --- default module
import sys
from multiprocessing import Process, Queue
import threading #threading for thread
import time

# --- installed module from pip
from PyQt5 import QtCore, QtGui, QtWidgets

# --- user defined module ---
# import windows to be displayed
from UI import MenuDisplay, TempInfoDisplay, MsgDisplay, AdminDeleteDisplay, AdminAddDisplay
import DataController

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

        #interrupt flag
        self.interrupt = False

        #init menu window
        MenuWindow = QtWidgets.QMainWindow()
        MenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler, {"menu_name":['사용자 메뉴', '관리자 메뉴'], "event_name":['userMenu', 'adminMenu']})
        MenuWindowUI.setupUi(MenuWindow)
        MenuWindow.show()

        #init admin menu window
        AdminMenuWindow = QtWidgets.QMainWindow()
        AdminMenuWindowUI = MenuDisplay.Ui_MenuWindow(self.menuEventHandler, {"menu_name":['추가', '삭제'], "event_name":['adminAdd', 'adminDelete']})
        AdminMenuWindowUI.setupUi(AdminMenuWindow)
        AdminMenuWindow.hide()

        #init tempInfo window
        TempInfoWindow = QtWidgets.QMainWindow()
        TempInfoWindowUI = TempInfoDisplay.Ui_TempInfoWindow(37.5, self.menuEventHandler)
        TempInfoWindowUI.setupUi(TempInfoWindow)
        TempInfoWindow.hide()

        #append windows
        self.windows['menuWindow'] = {"window" : MenuWindow, "ui" : MenuWindowUI}
        self.windows['adminMenuWindow'] = {"window":AdminMenuWindow, "ui":AdminMenuWindowUI}
        self.windows['tempInfoWindow'] = {"window":TempInfoWindow, "ui":TempInfoWindowUI}

        #thread
        self.thread = threading.Thread(target=self.isChanged, daemon=True)
        self.thread.start()

        self.init()

    def isChanged(self):
        while(True):
            time.sleep(0.5)
            if(self.dto.qsize()>0):
                print('is changed')
                item = self.dto.get()
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
                    #back to userMenu
                    self.menuEventHandler('userMenu')
                
             
    #select window to show for window transistion
    def selectWindow(self, new):
        before = self.windowsStack[-1]
        if(new != before):
            self.windows[before]['window'].hide()
        self.windowsStack.append(new)
        self.windows[new]['window'].show()

    #Handle events at windows
    def menuEventHandler(self, arg, others=None):
        self.requestQ.put(arg)
        if(arg == 'userMenu'):
            self.init()
            self.selectWindow('tempInfoWindow')
        
        elif(arg == 'adminMenu'):
            self.init()
            self.selectWindow('adminMenuWindow')

        elif(arg == 'adminAdd'):
            adminAddWindow = QtWidgets.QMainWindow()
            ui = AdminAddDisplay.Ui_MainWindow(self.menuEventHandler)
            ui.setupUi(adminAddWindow)
            ui.setStatus('사용자 추가 페이지입니다\n')
            ui.setUID('NFC 카드를 태그에 대주세요')
            adminAddWindow.show()
            self.windows['adminAddWindow'] = {'window':adminAddWindow, 'ui':ui}

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

        elif(arg == 'adminAdd_cancel'):
            self.windows['adminAddWindow']['window'].hide()
        
        elif(arg == 'adminDelete'):
            data = DataController.getUserData()
            print(data)
            adminDeleteWindow = QtWidgets.QMainWindow()
            ui = AdminDeleteDisplay.Ui_MainWindow(data, self.menuEventHandler)
            ui.setupUi(adminDeleteWindow)
            adminDeleteWindow.show()
            self.windows['adminDeleteWindow'] = {'window':adminDeleteWindow, 'ui':ui}
        
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
            else:
                pass

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

def Handler(requestQ, dto):
    while(True):
        time.sleep(0.5)
        if(requestQ.qsize()>0):
            item = requestQ.get()
            if(item == 'userMenu'):
                dto.put(RasberryController.getNameByNFC())
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