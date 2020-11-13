import sys, time
from multiprocessing import Process, Queue, Value
from threading import Thread
import RasberryController
import DataController

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ParentWidget(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)

        self.layout = QFormLayout()
        self.header = QHBoxLayout()
        self.layout.addRow(self.header)

        label = QLabel()
        pixmap = QPixmap('./resources/github.jpg').scaled(50, 50)
        label.setPixmap(pixmap)
        self.header.addWidget(label)

        text_label = QLabel("스테이터스")
        self.header.addWidget(text_label)

        self.setLayout(self.layout)

class InitialWidget(ParentWidget):
    def __init__(self):
        super().__init__()

        self.box = QHBoxLayout()
        self.setTitle("메뉴")

        self.layout.addRow(self.box)

        self.button = QPushButton('테스트')
        self.box.addWidget(self.button)

        self.setGeometry(0,0,500,500)
        self.mousePressEvent = lambda e : print('test ', e)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = InitialWidget()
    exit(app.exec_())