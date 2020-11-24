import sys
import time
from gtts import gTTS
from multiprocessing import Process, Queue, Value
from threading import Thread
from pathlib import Path
import RaspberryController
import DataController

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

'''
    ↓ TTS Class
'''


class TTS():
    def __init__(self):
        self.player = QMediaPlayer()

    def makeVoice(self, text):
        tts = gTTS(text=text, lang='ko')
        tts.save("./resources/tts/"+text+".mp3")

    def play(self, text):
        my_file = Path("./resources/tts/"+text+'.mp3')

        if (my_file.is_file() == False):
            print('not exist')
            self.makeVoice(text)

        self.filename = text+'.mp3'
        self.media = QUrl.fromLocalFile('./resources/tts/'+self.filename)
        self.content = QMediaContent(self.media)
        self.player.setMedia(self.content)
        self.player.play()


'''
    ↓ Header Widget
'''


class HeaderWidget(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        self.init_widget()

    def init_widget(self):
        # define layout
        self.header_layout = QHBoxLayout()  # Header 부분을 이룰 QHBoxLayout 이다.
        self.setLayout(self.header_layout)

        # define label
        self.header_label = QLabel("SSU CORONA PROJECT")

        # add components
        # header 레이아웃에 라벨을 달아준다.
        self.header_layout.addWidget(self.header_label)

        # set styles
        self.color1 = QColor(0, 0, 255)
        self.color2 = QColor(0, 0, 255)
        self.header_label_style = 'font-size:28px; font-family:Arial; font-weight:bold; color: white; margin-top: 5px; margin-bottom:5px; padding: 5px 0px;'
        self.header_label.setStyleSheet(self.header_label_style)
        self.header_label.setAlignment(Qt.AlignRight)

        # set animation
        self.animation = QVariantAnimation(
            self, valueChanged=self.animate, startValue=0.00001, endValue=1.0, duration=1000)

        # set background color
        self.setBackgroundColor()

    def animate(self, value):
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        self.header_label.setStyleSheet(self.header_label_style + grad)

    # do animation effect
    def animationStart(self):
        self.animation.setDirection(QAbstractAnimation.Forward)
        self.animation.start()

    # color must be QColor(r,g,b) type
    def setBackgroundColor(self, color1=None, color2=None):
        if(color1 != None):
            self.color1 = color1
        if(color2 != None):
            self.color2 = color2
        self.animationStart()


'''
    ↓ Initial Widget
'''


class InitialWidget(QGroupBox):
    def __init__(self, eventHandler):
        super().__init__()
        self.eventHandler = eventHandler

        self.init_widget()

    def init_widget(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.box = QHBoxLayout()
        self.layout.addRow(self.box)

        # style
        self_style = 'background:white;'
        self.setStyleSheet(self_style)
        self.box.setAlignment(Qt.AlignCenter)
        label_style = 'border'

        # define label
        self.label = QLabel()
        self.pixmap = QPixmap(
            './resources/img/logo_black.png').scaled(400, 400)
        self.label.setPixmap(self.pixmap)
        self.mousePressEvent = lambda e: self.eventHandler('init')

        # add Component
        self.box.addWidget(self.label)


'''
    ↓ Menu Widget
'''


class MenuWidget(QGroupBox):
    def __init__(self, menus, eventHandler, etc_button_event_name=None):
        super().__init__()

        self.menus = menus
        self.eventHandler = eventHandler
        self.etc_button_event_name = etc_button_event_name
        self.init_widget()

    def init_widget(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.box = QHBoxLayout()
        self.header = HeaderWidget()

        self.layout.addRow(self.header)
        self.layout.addRow(self.box)

        for menu in (self.menus):
            btn = QLabel(menu['menu_name'])
            # btn.resize(300,300)
            btn.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(
                f"./resources/img/{menu['menu_image']}").scaled(300, 300)
            btn.setPixmap(pixmap)
            handler_name = menu['menu_event_name']
            btn.mousePressEvent = lambda ch, handler_name=handler_name: self.eventHandler(
                handler_name)
            self.box.addWidget(btn)

        if(self.etc_button_event_name != None):
            self.cancel_button = QPushButton('뒤로 가기')
            self.cancel_button.setStyleSheet(
                'font-size: 20px; font-family:맑은 고딕; font-weight: bold; border: none; padding: 5px 0; color:blue;')
            self.cancel_button.clicked.connect(
                lambda ch, handler_name=self.etc_button_event_name: self.eventHandler(handler_name))
            self.layout.addRow(self.cancel_button)
        # style
        self.setStyleSheet("background: white;")
        self.header.setBackgroundColor(QColor(0, 0, 255), QColor(0, 0, 255))


'''
    ↓ NFC Wating Widget
'''


class NFCWatingWidget(QGroupBox):
    def __init__(self, menus, eventHandler):
        super().__init__()
        self.menus = menus
        self.eventHandler = eventHandler

        self.init_widget()

    def init_widget(self):
        # define layout
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.gif_box = QVBoxLayout()
        self.button_box = QHBoxLayout()
        self.header = HeaderWidget()

        # add sub-layout to layout
        self.layout.addRow(self.header)
        self.layout.addRow(self.gif_box)
        self.layout.addRow(self.button_box)

        # style
        self_style = 'background: white;'
        self.setStyleSheet(self_style)
        button_style = 'font-size: 20px; font-family:맑은 고딕; font-weight: bold; border: none; padding: 5px 0; color:blue;'
        label_style = 'font-size: 25px; font-family:맑은 고딕; font-weight: bold; padding: 10px 0;'

        # define components
        # - label for msg
        self.label = QLabel('하단의 리더기에 카드를 접촉해주십시오.')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(label_style)
        self.gif_box.addWidget(self.label)

        # - gif label
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)

        # - tagging_movie
        self.tagging_movie = QMovie('./resources/img/tagging.gif')
        self.tagging_movie.setScaledSize(QSize(400, 200))

        # - tagging_movie attach to gif label
        self.gif_label.setMovie(self.tagging_movie)
        self.tagging_movie.start()  # tagging.gif movie start
        self.gif_box.addWidget(self.gif_label)

        for menu in (self.menus):
            btn = QPushButton(menu['menu_name'])
            btn.setStyleSheet(button_style)
            handler_name = menu['menu_event_name']
            btn.clicked.connect(
                lambda ch, handler_name=handler_name: self.eventHandler(handler_name))
            self.button_box.addWidget(btn)

    # set status message

    def setStatus(self, status=None):
        if(status == None):
            self.label.setText('하단의 리더기에 카드를 접촉해주십시오')
        else:
            self.label.setText(status)


'''
    ↓ TempWidget
'''


class TempWidget(QGroupBox):
    def __init__(self):
        super().__init__()

        # define info
        self.name = ''
        self.id = ''
        self.belong = ''
        self.temp = ''
        self.status = ''

        # initializing widget
        self.init_widget()

    def init_widget(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.header = HeaderWidget()
        self.box = QVBoxLayout()

        # define label
        self.welcome_label = QLabel('')
        self.name_label = QLabel('')
        self.id_label = QLabel('')
        self.belong_label = QLabel('')
        self.temp_label = QLabel('')
        self.status_label = QLabel('')

        # alignment
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.box.setAlignment(Qt.AlignCenter)
        self.status_label.setAlignment(Qt.AlignCenter)

        # style
        self.setStyleSheet('background:white;')
        self.welcome_label.setStyleSheet('font-size:25px; font-family:맑은 고딕;')

        self.center_label_style = 'font-size:16px; font-family:맑은 고딕;'
        self.name_label.setStyleSheet(self.center_label_style)
        self.id_label.setStyleSheet(self.center_label_style)
        self.belong_label.setStyleSheet(self.center_label_style)
        self.temp_label.setStyleSheet(self.center_label_style)

        self.status_label.setStyleSheet(
            'font-size:20px; font-family:맑은 고딕; border:1px solid black;')

        # add component
        self.box.addWidget(QLabel())  # for spacing
        self.box.addWidget(self.name_label)
        self.box.addWidget(self.id_label)
        self.box.addWidget(self.belong_label)
        self.box.addWidget(self.temp_label)
        self.box.addWidget(QLabel())

        self.resize(700, 450)

        # assemble
        self.layout.addRow(self.header)
        self.layout.addRow(self.welcome_label)
        self.layout.addRow(self.box)
        self.layout.addRow(self.status_label)

    # name setter
    def setName(self, name):
        self.name = name
        if(self.name != None):
            self.welcome_label.setText('환영합니다, ' + self.name + '님')
            self.name_label.setText('이름 : ' + self.name)

    # id setter
    def setId(self, id):
        self.id = id
        if(self.id != None):
            self.id_label.setText('ID : ' + self.id)

    # belong setter
    def setBelong(self, belong):
        self.belong = belong
        if(self.belong != None):
            self.belong_label.setText('소속 : ' + self.belong)

    # temp setter
    def setTemp(self, temp):
        self.temp = temp
        if(self.temp != None):
            self.temp_label.setText('체온 : ' + self.temp + '℃')

    # status setter
    def setStatus(self, status):
        self.status = status
        if(self.status != None):
            self.status_label.setText(self.status)

    # all class member variable init as ''
    def clear(self):
        self.header.setBackgroundColor(QColor(0, 0, 255), QColor(0, 0, 255))
        self.setName('')
        self.setId('')
        self.setBelong('')
        self.setTemp('')
        self.setStatus('')


'''
    ↓ Login Widget
'''


class LoginWidget(QGroupBox):
    def __init__(self, eventHandler):
        QGroupBox.__init__(self)
        self.box = QFormLayout()
        self.setLayout(self.box)

        # define widgets
        self.titleLabel = QLabel('관리자 로그인')
        self.idLabel = QLabel('ID : ')
        self.idEditor = QLineEdit()
        self.passwordLabel = QLabel('PW : ')
        self.passwordEditor = QLineEdit()
        self.statusLabel = QLabel('')

        self.cancelButton = QPushButton('뒤로가기')
        self.addButton = QPushButton('로그인')
        horizonLayout = QHBoxLayout()
        horizonLayout.addWidget(self.cancelButton)
        horizonLayout.addWidget(self.addButton)

        # event handle
        self.cancelButton.clicked.connect(lambda: eventHandler('login_cancel'))
        self.addButton.clicked.connect(
            lambda: eventHandler('login_add', self.getElements()))

        # self.box.setContentsMargins(40, 100, 40, 0)
        labelStyle = "font-size:20px;font-family: 맑은 고딕;"
        titleStyle = 'font-size:25px;font-family: 맑은 고딕;font-weight:bold;margin-top:10px;margin-bottom:60px;'
        statusLabelStyle = labelStyle + "height:30px;"
        editorStyle = "font-size:20px;font-family: 맑은 고딕;"
        buttonStyle = "margin-top:90px; height: 50px; font-size:20px; font-family: 맑은 고딕;"

        # label style
        self.titleLabel.setStyleSheet(titleStyle)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.idLabel.setStyleSheet(labelStyle)
        self.passwordLabel.setStyleSheet(labelStyle)

        # status label style
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet(statusLabelStyle)

        # editor style
        self.idEditor.setStyleSheet(editorStyle)
        self.passwordEditor.setStyleSheet(editorStyle)

        # button style
        self.cancelButton.setStyleSheet(buttonStyle)
        self.addButton.setStyleSheet(buttonStyle)

        # add widgets to box
        self.box.addRow(self.titleLabel)
        self.box.addRow(self.idLabel, self.idEditor)
        self.box.addRow(self.passwordLabel, self.passwordEditor)
        self.box.addRow(horizonLayout)
        self.box.addRow(self.statusLabel)

    def setStatus(self, text):
        self.statusLabel.setText(str(text))

    def setId(self, id):
        self.idEditor.setText(str(id))

    def setPassword(self, password):
        self.passwordEditor.setText(str(password))

    def getElements(self):
        target = {}
        target['id'] = self.idEditor.text()
        target['password'] = self.passwordEditor.text()
        print('in getElements 431:', target)
        return target


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
        self.idLabel = QLabel('학번/아이디: ')
        self.idEditor = QLineEdit()
        self.statusLabel = QLabel('')

        self.cancelButton = QPushButton('뒤로가기')
        self.addButton = QPushButton('추가하기')
        horizonLayout = QHBoxLayout()
        horizonLayout.addWidget(self.cancelButton)
        horizonLayout.addWidget(self.addButton)

        # event handle
        self.cancelButton.clicked.connect(
            lambda: eventHandler('adminAdd_cancel'))
        self.addButton.clicked.connect(
            lambda: eventHandler('adminAdd_add', self.getElements()))

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
        self.idLabel.setStyleSheet(labelStyle)

        # status label style
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet(statusLabelStyle)

        # editor style
        self.nfcIdEditor.setStyleSheet(editorStyle)
        self.nameEditor.setStyleSheet(editorStyle)
        self.belongEditor.setStyleSheet(editorStyle)
        self.idEditor.setStyleSheet(editorStyle)

        # button style
        self.cancelButton.setStyleSheet(buttonStyle)
        self.addButton.setStyleSheet(buttonStyle)

        # add widgets to box
        self.box.addRow(self.nfcIdLabel, self.nfcIdEditor)
        self.box.addRow(self.nameLabel, self.nameEditor)
        self.box.addRow(self.belongLabel, self.belongEditor)
        self.box.addRow(self.idLabel, self.idEditor)
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

    # set id
    def setId(self, id):
        self.idEditor.setText(str(id))

    # set status label
    def setStatus(self, text):
        self.statusLabel.setText(str(text))

    # get text of all line editor
    def getElements(self):
        target = {}
        target['nfcId'] = self.nfcIdEditor.text()
        target['name'] = self.nameEditor.text()
        target['belong'] = self.belongEditor.text()
        target['id'] = self.idEditor.text()
        return target

    # clear all label and lineEditor
    def clear(self):
        self.setNFCID('')
        self.setName('')
        self.setBelong('')
        self.setId('')
        self.setStatus('')


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
            if(self.responseQ.qsize() > 0):
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
        self.resize(650, 400)
        self.widgetsList = {}
        self.widgetStack = QStackedWidget(self)
        self.init_widget()
        self.toCenter()
        self.show()

        # thread
        self.worker = Worker(self.responseQ)
        self.worker.new_signal.connect(self.responseHandler)
        self.worker.start()

        self.tts = TTS()

    @ pyqtSlot(dict)
    def responseHandler(self, item):
        if(item['type'] == 'GET_USER_INFO'):
            if(item['user_info'] == None):
                self.nfcWaitingWidget.setStatus('저장돼있지 않은 카드입니다')
                self.nfcWaitingWidget.header.setBackgroundColor(
                    QColor(255, 0, 0), QColor(0, 0, 255))
            elif(item['user_info'] == 'INTERRUPTED'):
                self.interrupt.value = False  # set interrupt as False
                return
            else:
                user_info = item['user_info']
                self.tempWidget.setName(user_info['name'])
                self.tempWidget.setBelong(user_info['belong'])
                if(user_info['id'] != None):
                    self.tempWidget.setId(user_info['id'])
                self.tempWidget.setStatus('손목을 온도센서에 가까이 대주세요')
                self.tempWidget.header.setBackgroundColor(
                    QColor(0, 176, 80), QColor(0, 0, 255))
                self.changeWidget('tempWidget')
                self.requestQ.put({'type': 'GET_TEMP'})

        elif(item['type'] == 'GET_TEMP'):
            if(item['temp'] == 'INTERRUPTED'):
                self.interrupt.value = False  # set interrupt as False
                return
            self.tempWidget.setTemp(str(item['temp']))
            if(item['temp'] > 37.5):
                self.tempWidget.header.setBackgroundColor(
                    QColor(255, 0, 0), QColor(0, 176, 80))
                self.tempWidget.setStatus('체온이 높습니다. 보건실에 방문해주세요.')
                self.tts.play('체온이 높습니다')
            else:
                self.tempWidget.header.setBackgroundColor(
                    QColor(0, 0, 255), QColor(0, 176, 80))
                self.tempWidget.setStatus('정상 체온입니다.')
                self.tts.play('정상 체온입니다')

        elif(item['type'] == 'USER_RE_INIT'):
            self.tempWidget.clear()
            self.nfcWaitingWidget.setStatus()
            self.nfcWaitingWidget.header.setBackgroundColor(
                QColor(0, 0, 255), QColor(0, 0, 255))
            self.changeWidget('nfcWaitingWidget')
            self.requestQ.put({'type': 'GET_USER_INFO'})

        elif(item['type'] == 'GET_NFCID'):
            id = item['nfcId']
            if(id == None):
                self.adminAddWidget.setStatus('NFC 카드를 인식하지 못했습니다.')
            elif(id == 'INTERRUPTED'):
                self.interrupt.value = False  # set interrupt as False
                return
            else:
                self.adminAddWidget.setNFCID(id)
                self.adminAddWidget.setStatus('NFC 카드 인식에 성공했습니다.')

        elif(item['type'] == 'LOGIN_ADD'):
            result = item['result']
            if(result == True):
                self.changeWidget('adminMenuWidget')
            else:
                self.loginWidget.setStatus('로그인에 실패했습니다.')
                self.loginWidget.setPassword('')

        elif(item['type'] == 'ADD_USER'):
            if(item['result']):
                self.adminAddWidget.setStatus('저장에 성공했습니다')
            else:
                self.adminAddWidget.setStatus('저장에 실패했습니다')
            self.interrupt.value = False  # set interrupt as False

        elif(item['type'] == 'GET_USER_LIST'):
            data = item['result']
            self.adminDeleteWidget.setData(data)
            self.adminDeleteWidget.setStatus('표를 가져왔습니다.')
            self.interrupt.value = False  # set interrupt as False

    # init widget

    def init_widget(self):
        self.setWindowTitle("IoT 체온 스캐너")
        widget_laytout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(widget_laytout)

        self.initialWidget = InitialWidget(self.eventHandler)
        self.menuWidget = MenuWidget([{'menu_name': '디스플레이 모드', 'menu_event_name': 'userMenu', 'menu_image': 'displaymode.png'}, {
            'menu_name': '관리 모드', 'menu_event_name': 'adminMenu', 'menu_image': 'prefermode.png'}], self.eventHandler)
        self.tempWidget = TempWidget()
        self.loginWidget = LoginWidget(self.eventHandler)
        self.adminMenuWidget = MenuWidget(
            [{'menu_name': '멤버 추가', 'menu_event_name': 'adminAdd', 'menu_image': 'add.png'}], self.eventHandler, 'adminMenu_cancel')
        self.adminAddWidget = AdminAddWidget(self.eventHandler)
        self.nfcWaitingWidget = NFCWatingWidget(
            [{'menu_name': '뒤로가기', 'menu_event_name': 'userMenu_cancel'}], self.eventHandler)

        self.widgetStack.addWidget(self.initialWidget)
        self.widgetsList['initialWidget'] = 0

        self.widgetStack.addWidget(self.menuWidget)
        self.widgetsList['menuWidget'] = 1

        self.widgetStack.addWidget(self.tempWidget)
        self.widgetsList['tempWidget'] = 2

        self.widgetStack.addWidget(self.adminMenuWidget)
        self.widgetsList['adminMenuWidget'] = 3

        self.widgetStack.addWidget(self.adminAddWidget)
        self.widgetsList['adminAddWidget'] = 4

        self.widgetStack.addWidget(self.nfcWaitingWidget)
        self.widgetsList['nfcWaitingWidget'] = 5

        self.widgetStack.addWidget(self.loginWidget)
        self.widgetsList['loginWidget'] = 6

        widget_laytout.addWidget(self.widgetStack)
        self.changeWidget('initialWidget')

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
        if(kind == 'init'):
            self.changeWidget('menuWidget')

        elif(kind == 'userMenu'):
            self.nfcWaitingWidget.header.setBackgroundColor(
                QColor(0, 0, 255), QColor(0, 0, 255))
            self.changeWidget('nfcWaitingWidget')
            self.requestQ.put({'type': 'GET_USER_INFO'})

        elif(kind == 'userMenu_cancel'):
            if(self.isReady.value == False):  # if background is running
                self.interrupt.value = True  # interrupt signal
                while(self.isReady.value == False):  # wait
                    time.sleep(0.2)
            self.changeWidget('menuWidget')

        elif(kind == 'adminMenu'):
            self.loginWidget.setId('')
            self.loginWidget.setPassword('')
            self.loginWidget.setStatus('')
            self.changeWidget('loginWidget')

        elif(kind == 'login_add'):
            # print(params)
            self.loginWidget.setStatus('로그인 중입니다...')
            self.requestQ.put(
                {'type': 'LOGIN_ADD', 'id': params['id'], 'password': params['password']})

        elif(kind == 'login_cancel'):
            self.changeWidget('menuWidget')

        elif(kind == 'adminMenu_cancel'):
            self.requestQ.put({'type': 'LOGOUT'})
            self.changeWidget('menuWidget')

        elif(kind == 'adminAdd'):
            self.adminAddWidget.clear()
            self.adminAddWidget.setStatus('NFC 카드를 대주세요.')
            self.changeWidget('adminAddWidget')
            self.requestQ.put({'type': 'GET_NFCID'})

        elif(kind == 'adminAdd_cancel'):
            if(self.isReady.value == False):  # if background is running
                self.interrupt.value = True  # interrupt signal
                while(self.isReady.value == False):  # wait
                    time.sleep(0.2)
            self.adminAddWidget.clear()
            self.adminAddWidget.setStatus('')
            self.changeWidget('adminMenuWidget')

        elif(kind == 'adminAdd_add'):
            self.adminAddWidget.setStatus('처리중입니다.')
            self.requestQ.put(
                {'type': 'ADD_USER', 'nfcId': params['nfcId'], 'name': params['name'], 'belong': params['belong'], 'id': params['id']})


'''
    ↓ Handler Function for Background Process
'''


def Handler(requestQ, responseQ, interrupt, isReady):
    dataController = DataController.DataController(interrupt)
    raspberryController = RaspberryController.RaspberryController(interrupt)
    id = None
    temp = None
    show_time = 4  # seconds

    while(True):
        time.sleep(1)
        # print('running')
        if(requestQ.qsize() > 0):
            item = requestQ.get()
            isReady.value = False  # set flag false when working...

            # Get nfc id and name
            if(item['type'] == 'GET_USER_INFO'):
                id = raspberryController.getNFCId()  # for propagation interrupt signal
                if(id == 'INTERRUPTED'):
                    responseQ.put({'type': 'GET_USER_INFO', 'user_info': id})
                else:
                    user_info = dataController.getUserDataByNFC(id)
                    if(interrupt.value != True):
                        responseQ.put(
                            {'type': 'GET_USER_INFO', 'user_info': user_info})
                    # print(user_info)
                    if(user_info == None):
                        time.sleep(show_time)
                        responseQ.put({'type': 'USER_RE_INIT'})

            # Get temperature And Re init
            elif(item['type'] == 'GET_TEMP'):
                temp = raspberryController.getTemp()  # for propagation interrupt signal
                if(id != 'INTERRUPTED' and temp != 'INTERRUPTED'):
                    result = dataController.addTempData(id, temp)
                responseQ.put({'type': 'GET_TEMP', 'temp': temp})
                time.sleep(show_time)
                responseQ.put({'type': 'USER_RE_INIT'})

            elif(item['type'] == 'GET_NFCID'):
                id = raspberryController.getNFCId()  # for propagation interrupt signal
                responseQ.put({'type': 'GET_NFCID', 'nfcId': id})

            elif(item['type'] == 'ADD_USER'):
                result = dataController.addUser(
                    item['nfcId'], item['name'], item['belong'], item['id'])
                responseQ.put({'type': 'ADD_USER', 'result': result})

            elif(item['type'] == 'GET_USER_LIST'):
                result = dataController.getUserData()
                responseQ.put({'type': 'GET_USER_LIST', 'result': result})

            elif(item['type'] == 'LOGIN_ADD'):
                print(item['id'], ' ', item['password'])
                result = dataController.login(item['id'], item['password'])
                print('login result in handler:', result)
                responseQ.put({'type': 'LOGIN_ADD', 'result': result})

            elif(item['type'] == 'LOGOUT'):
                dataController.logout()

            isReady.value = True  # set flag true when ready


if __name__ == "__main__":
    app = QApplication(sys.argv)

    requestQ = Queue()
    responseQ = Queue()
    interrupt = Value('b', False)
    isReady = Value('b', True)
    view = View(requestQ, responseQ, interrupt, isReady)

    background = Process(target=Handler, args=(
        requestQ, responseQ, interrupt, isReady), daemon=True)
    background.start()

    exit(app.exec_())
