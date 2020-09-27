import time
import threading
from PyQt5 import QtCore

import DataController
class RasberryController(threading.Thread):
    def __init__(self, dto, threadEvent=None, category=None):
        threading.Thread.__init__(self)
        self.dataController = DataController.DataController()
        self.category = category
        self.dto = dto
        self.threadEvent = threadEvent

    def __del__(self):
        print('---end----')

    def run(self):
        if(self.category == 'NFC'):
            self.getNFC()
        elif(self.category == 'temp'):
            self.getTemp()
        if(self.threadEvent != None):
            self.threadEvent()
        

    def setCategory(self, category):
        self.category = category

    def getNFC(self):
        time.sleep(1)
        self.dto['uid'] = 12345678
        self.dto['name'] = '홍길동'

    def getTemp(self):
        time.sleep(3)
        self.dto['temp'] = 36.5
