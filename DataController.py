import requests
import time

URL = 'http://localhost:3000/rest'

def getNameByNFC(uid):
    if(uid == 12345678):
        return '홍길동'