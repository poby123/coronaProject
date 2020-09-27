import time
from PyQt5 import QtCore

import DataController
class RasberryController(QtCore.QThread):
    def __init__(self, threadEndEvent, category, parent=None):
        super(RasberryController, self).__init__(parent)
        self.threadEndEvent = threadEndEvent #props from DisplayController
        self.dataController = DataController.DataController()
        self.category = category #mean which sensor use

    def __del__(self):
        print('---end----')

    def run(self):
        if(self.category == 'NFC'):
            self.getNFC()

    def getNFC(self):
        time.sleep(3)
        uid = 12345678
        name = self.dataController.getNameByNFC(uid)
        self.threadEndEvent(self.category, uid, name)

    def getTemp(self):
        time.sleep(3)
        # self.uid[0] = 12345678
