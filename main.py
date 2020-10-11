import sys, time
from multiprocessing import Process, Queue, Value
from threading import Thread
import RasberryController
import DataController

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
    ↓ Menu Widget
'''
class MenuWidget(QGroupBox):
    def __init__(self, menu1, menu2, eventName1, eventName2, eventHandler):
        QGroupBox.__init__(self)

        self.box = QHBoxLayout()
        self.setLayout(self.box)
        self.setTitle("메뉴")
        
        #define button
        btn1 = QPushButton(menu1)
        btn2 = QPushButton(menu2)

        #style
        self.setStyleSheet("background: white;")
        buttonStyle = "height : 300px; \
            border-width:5px; border-color:blue; border-radius: 10px; border-style:solid; \
            background: white; \
            font-size: 30px; font-weight: bold; font-family: 맑은 고딕;"
        btn1.setStyleSheet(buttonStyle)
        btn2.setStyleSheet(buttonStyle)

        # add event handler
        btn1.clicked.connect(lambda : eventHandler(eventName1))
        btn2.clicked.connect(lambda : eventHandler(eventName2))
        
        # add buttons to box
        self.box.addWidget(btn1)
        self.box.addWidget(btn2)

'''
    ↓ TempWidget
'''
class TempWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        self.box = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.box)
        self.setTitle("체온 확인")

        # define label
        self.name = QLabel('이름과 소속')
        self.temp = QLabel('체온')
        self.status = QLabel('확인중입니다')
        self.cancelButton = QPushButton('뒤로가기')

        # event 
        self.cancelButton.clicked.connect(lambda : eventHandler('userMenu_cancel'))

        # alignment
        self.name.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.status.setAlignment(Qt.AlignCenter)

        # style
        labelStyle = "background: white; font-size: 25px; font-family: 맑은 고딕; border-width:3px; border-style:solid; border-color:black;"
        self.name.setStyleSheet(labelStyle)
        self.temp.setStyleSheet(labelStyle)
        self.status.setStyleSheet(labelStyle)

        # add labels to box
        self.box.addWidget(self.name)
        self.box.addWidget(self.temp)
        self.box.addWidget(self.status)
        self.box.addWidget(self.cancelButton)

    def setName(self, name):
        self.name.setText(name)

    def getName(self):
        return self.name.text()
    
    def setTemp(self, temperature):
        self.temp.setText(temperature)
    
    def getTemp(self):
        return self.temp.text()
    
    def setStatus(self, status):
        self.status.setText(status)
    
    def getStatus(self):
        return self.status.text()

    def clear(self):
        self.setName('')
        self.setTemp('')
        self.setStatus('')

'''
    ↓ AdminAdd Widget
'''
class AdminAddWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        self.box = QFormLayout()
        self.setLayout(self.box)
        self.setTitle("멤버 추가")

        # define widgets
        self.nfcIdLabel = QLabel('NFC ID : ')
        self.nfcIdEditor = QLineEdit()
        self.nameLabel = QLabel('이름 : ')
        self.nameEditor = QLineEdit()
        self.belongLabel = QLabel('소속 : ')
        self.belongEditor = QLineEdit()
        self.statusLabel = QLabel('')

        self.cancelButton = QPushButton('뒤로가기')
        self.addButton = QPushButton('추가하기')
        horizonLayout = QHBoxLayout()
        horizonLayout.addWidget(self.cancelButton)
        horizonLayout.addWidget(self.addButton)

        # event handle
        self.cancelButton.clicked.connect(lambda :eventHandler('adminAdd_cancel'))
        self.addButton.clicked.connect(lambda : eventHandler('adminAdd_add', self.getElements()))

        # define style
        self.box.setContentsMargins(40, 100, 40, 0)
        labelStyle = "font-size:20px;font-family: 맑은 고딕;"
        statusLabelStyle = labelStyle + "height:30px;"
        editorStyle = "font-size:20px;font-family: 맑은 고딕;"
        buttonStyle = "margin-top:90px; height: 50px; font-size:20px; font-family: 맑은 고딕;"

        # label style
        self.nfcIdLabel.setStyleSheet(labelStyle)
        self.nameLabel.setStyleSheet(labelStyle)
        self.belongLabel.setStyleSheet(labelStyle)

        # status label style
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet(statusLabelStyle)

        # editor style
        self.nfcIdEditor.setStyleSheet(editorStyle)
        self.nameEditor.setStyleSheet(editorStyle)
        self.belongEditor.setStyleSheet(editorStyle)
        
        #button style
        self.cancelButton.setStyleSheet(buttonStyle)
        self.addButton.setStyleSheet(buttonStyle)

        # add widgets to box
        self.box.addRow(self.nfcIdLabel, self.nfcIdEditor)
        self.box.addRow(self.nameLabel, self.nameEditor)
        self.box.addRow(self.belongLabel, self.belongEditor)
        self.box.addRow(horizonLayout)
        self.box.addRow(self.statusLabel)

    # set nfc id
    def setNFCID(self, id):
        self.nfcIdEditor.setText(str(id))

    # set name
    def setName(self, name):
        self.nameEditor.setText(str(name))

    # set belong
    def setBelong(self, belong):
        self.belongEditor.setText(str(belong))

    # set status label
    def setStatus(self, text):
        self.statusLabel.setText(str(text))

    # get text of all line editor
    def getElements(self):
        target = {}
        target['nfcId'] = self.nfcIdEditor.text()
        target['name'] = self.nameEditor.text()
        target['belong'] = self.belongEditor.text()
        return target

    # clear all label and lineEditor
    def clear(self):
        self.setNFCID('')
        self.setName('')
        self.setBelong('')
        self.setStatus('')

'''
    ↓ AdminDeleteWidget
'''
class AdminDeleteWidget(QGroupBox):
    def __init__(self, eventHandler, data=None):
        QGroupBox.__init__(self)
        #props 
        self.eventHandler = eventHandler
        if(data != None):
            self.data = data
        else : 
            self.data = []
        self.checkBoxs = []
        self.targets = []
        self.init_widget()
    
    def init_widget(self):
        self.box = QFormLayout()
        hbox = QHBoxLayout()
        self.setLayout(self.box)
        self.setTitle("멤버 삭제")

        # define widgets
        self.table = QTableWidget(len(self.data),4)
        self.table.setHorizontalHeaderLabels(["이름", "소속", "NFC ID", "삭제"])
        self.cancelButton = QPushButton('뒤로가기')
        self.deleteButton = QPushButton('삭제하기')
        self.statusLabel = QLabel('')

        # button event handler
        self.cancelButton.clicked.connect(lambda : self.eventHandler('adminDelete_cancel'))
        self.deleteButton.clicked.connect(lambda : self.eventHandler('adminDelete_delete',  self.getSelected()))

        # style
        buttonStyle = "height:40px; font-size: 20px; font-family: 맑은 고딕;"
        self.cancelButton.setStyleSheet(buttonStyle)
        self.deleteButton.setStyleSheet(buttonStyle)

        labelStyle = 'font-family: 맑은 고딕; font-size:20px;'
        self.statusLabel.setStyleSheet(labelStyle)

        # add widgets to box
        self.box.addWidget(self.table)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.deleteButton)
        self.box.addRow(hbox)
        self.box.addRow(self.statusLabel)

        self.drawTable()

    # data setter
    def setData(self, data):
        self.table.clearContents()
        self.data = data
        self.drawTable()
        
    # resize header with content
    def resizeHeaderWidth(self):
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    # draw table
    def drawTable(self):
        self.table.setRowCount(len(self.data))
        i = 0
        self.checkBoxs = []
        for current in self.data:
            nameLabel = QLabel(current['name'])
            belongLabel = QLabel(current['belong'])
            nfcLabel = QLabel(current['nfcid'])
            checkbox = MyCheckBox(current['nfcid'])
            
            self.checkBoxs.append(checkbox)

            self.table.setCellWidget(i,0,nameLabel)
            self.table.setCellWidget(i,1, belongLabel)
            self.table.setCellWidget(i,2, nfcLabel)

            checkBoxCellWidget = QWidget()
            lay_out = QHBoxLayout(checkBoxCellWidget)
            lay_out.addWidget(checkbox)
            lay_out.setAlignment(Qt.AlignCenter)
            lay_out.setContentsMargins(0,0,0,0)
            checkBoxCellWidget.setLayout(lay_out)
            self.table.setCellWidget(i,3, checkBoxCellWidget)

            i += 1
        self.resizeHeaderWidth()
    
    # get selected nfc id
    def getSelected(self): 
        for box in self.checkBoxs:
            if(box.getUID() != False):
                self.targets.append(box.getUID())
        return self.targets

    # update data after delete data element
    def removeTargetData(self):
        self.data = list(filter(lambda item: item['nfcid'] not in self.targets, self.data))
        self.targets.clear()

    # set status text at label
    def setStatus(self, status):
        self.statusLabel.setText(status)
        
'''
    ↓ My Checkbox for Admin Delete Widget
'''
class MyCheckBox(QCheckBox):
    def __init__(self, nfcId):
        super().__init__()
        self.nfcId = nfcId
        self.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")

    def getUID(self):
        if(self.isChecked()):
            return self.nfcId
        else :
            return False        

'''
    ↓ Thread Worker Class
'''
class Worker(QThread):
    new_signal = pyqtSignal(dict)

    def __init__(self, responseQ):
        super().__init__()
        self.responseQ = responseQ

    def run(self):
        while(True):
            time.sleep(1)
            if(self.responseQ.qsize()>0):
                item = self.responseQ.get()
                self.new_signal.emit(item)

'''
    ↓ Widgets Controller
'''
class View(QWidget):
    def __init__(self, requestQ, responseQ, interrupt, isReady):
        QWidget.__init__(self, flags=Qt.Widget)

        # props initialize
        self.requestQ = requestQ
        self.responseQ = responseQ
        self.interrupt = interrupt
        self.isReady = isReady

        # window initialize
        self.resize(700,450)
        self.widgetsList = {}
        self.widgetStack = QStackedWidget(self)
        self.init_widget()
        self.toCenter()
        self.show()

        # thread
        self.worker = Worker(self.responseQ)
        self.worker.new_signal.connect(self.responseHandler)
        self.worker.start()
    
    @pyqtSlot(dict)
    def responseHandler(self, item):
        if(item['type'] == 'GET_NAME'):
            if(item['name'] == None):
                self.tempWidget.setStatus('저장돼있지 않은 카드입니다')
            elif(item['name'] == 'INTERRUPTED'):
                self.interrupt.value = False # set interrupt as False
                return
            else:
                self.tempWidget.setName(item['name'])
                self.tempWidget.setStatus('손목을 온도센서에 가까이 대주세요')
                self.requestQ.put({'type':'GET_TEMP'})

        elif(item['type'] == 'GET_TEMP'):
                if(item['temp'] == 'INTERRUPTED'):
                    self.interrupt.value = False # set interrupt as False
                    return
                self.tempWidget.setTemp(str(item['temp']))
                if(item['temp'] > 37.5):
                    self.tempWidget.setStatus('체온이 높습니다. 보건실에 방문해주세요.')
                else:
                    self.tempWidget.setStatus('정상 체온입니다.')
                # 초기화 후 반복처리

        elif(item['type']=='GET_NFCID'):
            id = item['nfcId']
            if(id == None):
                self.adminAddWidget.setStatus('NFC 카드를 인식하지 못했습니다.')
            elif(id == 'INTERRUPTED'):
                self.interrupt.value = False # set interrupt as False
                return
            else:
                self.adminAddWidget.setNFCID(id)
                self.adminAddWidget.setStatus('NFC 카드 인식에 성공했습니다.')

        elif(item['type']=='ADD_USER'):
            if(item['result']):
                self.adminAddWidget.setStatus('저장에 성공했습니다')
            else:
                self.adminAddWidget.setStatus('저장에 실패했습니다')
            self.interrupt.value = False # set interrupt as False

        elif(item['type']=='GET_USER_LIST'):
            data = item['result']
            self.adminDeleteWidget.setData(data)
            self.adminDeleteWidget.setStatus('표를 가져왔습니다.')
            self.interrupt.value = False # set interrupt as False

        elif(item['type']=='DELETE_USER'):
            if(item['result']):
                self.adminDeleteWidget.setStatus('삭제에 성공했습니다.')
                self.adminDeleteWidget.removeTargetData()
                self.adminDeleteWidget.drawTable()
            else:
                self.adminDeleteWidget.setStatus('삭제에 실패했습니다')
            self.interrupt.value = False # set interrupt as False
        

    # init widget
    def init_widget(self):
        self.setWindowTitle("Body Temperature Scanner")
        widget_laytout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(widget_laytout)

        self.menuWidget = MenuWidget('사용자 메뉴', '관리자 메뉴', 'userMenu','adminMenu', self.eventHandler)
        self.tempWidget = TempWidget(self.eventHandler)
        self.adminMenuWidget = MenuWidget('멤버 추가', '멤버 삭제','adminAdd','adminDelete', self.eventHandler)
        self.adminAddWidget = AdminAddWidget(self.eventHandler)
        self.adminDeleteWidget = AdminDeleteWidget(self.eventHandler)

        self.widgetStack.addWidget(self.menuWidget)
        self.widgetsList['menuWidget'] = 0
        
        self.widgetStack.addWidget(self.tempWidget)
        self.widgetsList['tempWidget'] = 1
        
        self.widgetStack.addWidget(self.adminMenuWidget)
        self.widgetsList['adminMenuWidget'] = 2

        self.widgetStack.addWidget(self.adminAddWidget)
        self.widgetsList['adminAddWidget'] = 3

        self.widgetStack.addWidget(self.adminDeleteWidget)
        self.widgetsList['adminDeleteWidget'] = 4

        widget_laytout.addWidget(self.widgetStack)
        self.changeWidget('menuWidget')

    # move window to center point of display
    def toCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # change displayed widget
    def changeWidget(self, target):
        self.widgetStack.setCurrentIndex(self.widgetsList[target])

    # event handle that causes widgets
    def eventHandler(self, kind, params=None):
        if(kind == 'userMenu'):
            self.tempWidget.clear()
            self.tempWidget.setStatus('NFC 카드를 대주세요.')
            self.changeWidget('tempWidget')
            self.requestQ.put({'type':'GET_NAME'})

        elif(kind == 'userMenu_cancel'):
            if(self.isReady.value == False): # if background is running
                self.interrupt.value = True # interrupt signal
                while(self.isReady.value == False): # wait
                    time.sleep(0.2)
            self.changeWidget('menuWidget')

        elif(kind == 'adminMenu'):
            self.changeWidget('adminMenuWidget')
        
        elif(kind == 'adminAdd'):
            self.adminAddWidget.clear()
            self.adminAddWidget.setStatus('NFC 카드를 대주세요.')
            self.changeWidget('adminAddWidget')
            self.requestQ.put({'type':'GET_NFCID'})
        
        elif(kind == 'adminDelete'):
            self.adminDeleteWidget.setStatus('표를 불러오는 중입니다.')
            self.changeWidget('adminDeleteWidget')
            self.requestQ.put({'type':'GET_USER_LIST'})
        
        elif(kind == 'adminAdd_cancel'):
            if(self.isReady.value == False): # if background is running
                self.interrupt.value = True # interrupt signal
                while(self.isReady.value == False): # wait
                    time.sleep(0.2)
            self.adminAddWidget.clear()
            self.adminAddWidget.setStatus('')
            self.changeWidget('adminMenuWidget')
        
        elif(kind == 'adminAdd_add'):
            self.adminAddWidget.setStatus('처리중입니다.')
            self.requestQ.put({'type':'ADD_USER', 'nfcId':params['nfcId'], 'name':params['name'], 'belong':params['belong']})
        
        elif(kind == 'adminDelete_cancel'):
            while(self.isReady.value == False): # wait
                    time.sleep(0.2)
            self.changeWidget('adminMenuWidget')
        
        elif(kind == 'adminDelete_delete'):
            self.adminDeleteWidget.setStatus('삭제중입니다. 잠시 기다려주세요')
            self.requestQ.put({'type':'DELETE_USER', 'target':params})

'''
    ↓ Handler Function for Background Process
'''
def Handler(requestQ, responseQ, interrupt, isReady):
    dataController = DataController.DataController(interrupt)
    id = None
    temp = None

    while(True):
        time.sleep(1)
        print('running')
        if(requestQ.qsize() > 0):
            item = requestQ.get()
            isReady.value = False #set flag false when working...

            # Get nfc id and name
            if(item['type'] == 'GET_NAME'):
                id = RasberryController.getNFCId(interrupt) # for propagation interrupt signal
                if(id == 'INTERRUPTED'):
                    responseQ.put({'type':'GET_NAME', 'name':id})
                else:
                    name = dataController.getNameByNFC(id)
                    responseQ.put({'type':'GET_NAME', 'name':name})
            
            # Get temperature
            elif(item['type'] == 'GET_TEMP'):
                temp = RasberryController.getTemp(interrupt) # for propagation interrupt signal
                if(id != 'INTERRUPTED' and temp != 'INTERRUPTED'):
                    result = dataController.addTempData(id, temp)
                responseQ.put({'type':'GET_TEMP', 'temp':temp})

            elif(item['type']=='GET_NFCID'):
                id = RasberryController.getNFCId(interrupt) # for propagation interrupt signal
                responseQ.put({'type':'GET_NFCID', 'nfcId':id})

            elif(item['type']=='ADD_USER'):
                result = dataController.addUser(item['nfcId'], item['name'], item['belong'])
                responseQ.put({'type':'ADD_USER', 'result':result})

            elif(item['type']=='GET_USER_LIST'):
                result = dataController.getUserData()
                responseQ.put({'type':'GET_USER_LIST', 'result':result})

            elif(item['type']=='DELETE_USER'):
                result = dataController.deleteUser(item['target'])
                responseQ.put({'type':'DELETE_USER', 'result':result})
        
            isReady.value = True # set flag true when ready


if __name__ == "__main__":
    app = QApplication(sys.argv)
    requestQ = Queue()
    responseQ = Queue()
    interrupt = Value('b', False)
    isReady = Value('b', True)
    view = View(requestQ, responseQ, interrupt, isReady)

    background = Process(target=Handler, args=(requestQ, responseQ, interrupt, isReady), daemon=True)
    background.start()

    exit(app.exec_())