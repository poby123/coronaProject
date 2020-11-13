import sys, time
from multiprocessing import Process, Queue, Value
from threading import Thread
import RasberryController
import DataController

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
    ↓ Header Widget
'''
class HeaderWidget(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        self.init_widget()

    def init_widget(self):
        # define layout
        self.header_layout = QHBoxLayout() # Header 부분을 이룰 QHBoxLayout 이다.
        self.setLayout(self.header_layout)

        # define label
        self.header_label = QLabel("SSU CORONA PROJECT")

        # add components
        self.header_layout.addWidget(self.header_label) #header 레이아웃에 라벨을 달아준다.

        # set styles
        self.color1 = QColor(0,0,255)
        self.color2 = QColor(0,0,255)
        self.header_label_style = 'font-size:28px; font-family:Arial; font-weight:bold; color: white; margin-top: 20px; margin-bottom:20px; padding: 10px 0px;'
        self.header_label.setStyleSheet(self.header_label_style)
        self.header_label.setAlignment(Qt.AlignRight)

        #set animation
        self.animation = QVariantAnimation(self, valueChanged=self.animate, startValue=0.00001, endValue=1.0, duration=1000)
        
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

    #color must be QColor(r,g,b) type
    def setBackgroundColor(self,color1=None, color2=None):
        if(color1 != None):
            self.color1 = color1
        if(color2 != None):
            self.color2 = color2
        self.animationStart()

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
        self.welcome_label = QLabel()
        self.name_label = QLabel()
        self.id_label = QLabel()
        self.belong_label = QLabel()
        self.temp_label = QLabel()
        self.status_label = QLabel()

        # alignment
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.box.setAlignment(Qt.AlignCenter)
        self.status_label.setAlignment(Qt.AlignCenter)

        # style
        self.setStyleSheet('background:white;')
        self.welcome_label.setStyleSheet('font-size:25px; font-family:맑은 고딕;')
        self.center_label_style = 'font-size:16px; font-family:맑은 고딕; padding-left:5em; '
        self.name_label.setStyleSheet(self.center_label_style)
        self.id_label.setStyleSheet(self.center_label_style)
        self.belong_label.setStyleSheet(self.center_label_style)
        self.temp_label.setStyleSheet(self.center_label_style)

        self.status_label.setStyleSheet('font-size:20px; font-family:맑은 고딕; border:1px solid black;')


        # add component
        self.box.addWidget(QLabel())
        self.box.addWidget(self.welcome_label)
        self.box.addWidget(QLabel())
        self.box.addWidget(self.name_label)
        self.box.addWidget(self.id_label)
        self.box.addWidget(self.belong_label)
        self.box.addWidget(self.temp_label)
        self.box.addWidget(QLabel())
        self.box.addWidget(self.status_label)

        self.resize(700,450)

        # assemble
        self.layout.addRow(self.header)
        self.layout.addRow(self.box)

        # self.setName('홍길동')
        # self.setId('20201753')
        # self.setBelong('숭실대학교 IT대학 소프트웨어학부')
        # self.setTemp('36.8')
        # self.setStatus('손목을 체온기에 가까이 대주세요')

    # name setter
    def setName(self, name):
        self.name = name
        if(self.name != None):
            self.welcome_label.setText('환영합니다, '+ self.name + '님')
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
        self.setName('')
        self.setId('')
        self.setBelong('')
        self.setTemp('')
        self.setStatus('')

def eventHandler():
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    temp = TempWidget()
    temp.show()

    exit(app.exec_())