import time
import threading
from PyQt5 import QtCore
from multiprocessing import Queue
import DataController

def getNFC():
    # dataController = DataController()
    # for i in range(1, 10000000):
    #     pass
    time.sleep(2)
    dto = {}
    dto['type'] = 'NFC'
    dto['uid'] = 12345678
    dto['name'] = DataController.getNameByNFC(dto['uid'])
    dto['temp'] = None
    return dto

def getTemp():
    for i in range(1, 100000000):
        pass
    dto = {}
    dto['type'] = 'TEMP'
    dto['uid'] = None
    dto['name'] = None
    dto['temp'] = 37.8
    return dto
    

if __name__ == '__main__':
    q = Queue()
    getNFC(q)
    print(q.get())
