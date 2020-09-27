import time
import threading
from PyQt5 import QtCore

import DataController
class RasberryController(threading.Thread, threading.Event):
    def __init__(self, dto, threadEvent=None, category=None):
        threading.Thread.__init__(self, daemon=True)
        self.dataController = DataController.DataController()
        self.category = category
        self.dto = dto
        self.threadEvent = threadEvent
        self.interrupt = False

    def __del__(self):
        print('---end----')

    def run(self):
        if(self.interrupt):
            return
        elif(self.category == 'NFC'):
            self.getNFC()
        elif(self.category == 'temp'):
            self.getTemp()
        if(self.threadEvent != None):
            self.threadEvent()

    def setCategory(self, category):
        self.category = category

    def reset(self):
        self.interrupt = False

    def stop(self):
        self.interrupt = True

    def getNFC(self):
        for i in range(1, 10000):
            pass
            if(self.interrupt):
                return
        self.dto['uid'] = 12345678
        self.dto['name'] = self.dataController.getNameByNFC(self.dto['uid'])

    def getTemp(self):
        for i in range(1, 10000):
            pass
            if(self.interrupt):
                return
        self.dto['temp'] = 36.5
