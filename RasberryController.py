import time
from multiprocessing import Value

# def getNameByNFC(id):
#     time.sleep(3)
#     dto = {}
#     dto['type'] = 'NFC_NAME'
#     dto['uid'] = 1234
#     dto['name'] = DataController.getNameByNFC(dto['uid'])
#     dto['temp'] = None
#     return dto

def getNFCId(interrupt):
    for i in range(3):
        if(interrupt.value):
            return 'INTERRUPTED'
        else:
            time.sleep(1)
    return 12345678

def getTemp(interrupt):
    for i in range(3):
        if(interrupt.value):
            return 'INTERRUPTED'
        time.sleep(1)
    return 37.3
