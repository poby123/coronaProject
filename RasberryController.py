import time
from multiprocessing import Queue

# def getNameByNFC(id):
#     time.sleep(3)
#     dto = {}
#     dto['type'] = 'NFC_NAME'
#     dto['uid'] = 1234
#     dto['name'] = DataController.getNameByNFC(dto['uid'])
#     dto['temp'] = None
#     return dto

def getNFCId():
    time.sleep(2)
    return 1234567

def getTemp():
    time.sleep(2)
    return 37.3
