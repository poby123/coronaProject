import time
from multiprocessing import Value

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
    return 37.2
