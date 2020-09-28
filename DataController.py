import requests
import time

class DataController():
    def __init__(self):
        self.URL = 'http://localhost:3000/rest'

    def getNameByNFC(self, uid):
        if(uid == 12345678):
            return '홍길동'