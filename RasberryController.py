import time
from multiprocessing import Queue
import DataController

def getNameByNFC():
    time.sleep(3)
    dto = {}
    dto['type'] = 'NFC_NAME'
    dto['uid'] = 1234
    dto['name'] = DataController.getNameByNFC(dto['uid'])
    dto['temp'] = None
    return dto

def getNFCId(interrupt):
    print('get NFC ID is called in Rasberry Controller')
    dto = {}
    dto['type'] = 'NFC_ID'
    dto['name'] = None
    dto['temp'] = None

    for i in range(5):
        time.sleep(1)
        print('getNFCID is running')
        if(interrupt.qsize()>0):
            item = interrupt.get()
            print(item)
            dto['type'] = "INTERRUPT"
            return dto

    dto['uid'] = 12345678
    return dto

def getTemp():
    time.sleep(3)
    dto = {}
    dto['type'] = 'TEMP'
    dto['uid'] = None
    dto['name'] = None
    dto['temp'] = 37.4
    return dto
