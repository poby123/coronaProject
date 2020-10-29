import requests, json
import time
from multiprocessing import Value

class DataController():

    def __init__(self, interrupt=None):
        # self.URL = 'https://ssu-corona.herokuapp.com/rest' 
        self.URL = 'http://localhost:3000/rest'
        if(interrupt!=None):
            self.interrupt = interrupt

    def getUserDataByNFC(self, nfcId):
        params = {'nfcId':nfcId}
        response = requests.get(self.URL + '/identify', params=params)
        state = response.status_code
        result = response.json()
        if(result['result'] == True):
            return result['obj']
        else:
            return None

    def addTempData(self, nfcId, temp):
        params = {'nfcId':nfcId, 'temperature':temp}
        response = requests.get(self.URL + '/addTempData', params=params)
        state = response.status_code
        result = response.json()
        print(result)

    def addUser(self, nfcId, name, belong, id):
        data = {'target': {'nfcId':nfcId, 'name':name, 'belong' : belong, 'id': id}}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(self.URL + '/addUser', headers=headers ,data=json.dumps(data))
        state = response.status_code
        result = response.json()
        return result['result']

    def deleteUser(self,targets):
        data = {'target': targets}
        response = requests.post(self.URL + '/deleteUser', data=data)
        result = response.json()
        return result['result']

    def getUserData(self):
        time.sleep(1)
        response = requests.get(self.URL + '/userInfoWithoutTemp')
        state = response.status_code
        result = response.json()
        if(result['result'] == True):
            return result['content']
        else:
            return None

if __name__ == '__main__':
    dc = DataController()
    # print(dc.addUser('12345678', '이름 테스트', '소속 테스트'))
    print(dc.getUserDataByNFC(1234))
    