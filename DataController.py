import requests
import time

class DataController():

    def __init__(self):
        self.URL = 'https://ssu-corona.herokuapp.com/rest' 

    def getNameByNFC(self, nfcId):
        params = {'nfcId':nfcId}
        response = requests.get(self.URL + '/identify', params=params)
        state = response.status_code
        result = response.json()
        if(result['result'] == True):
            return result['name']
        else:
            return None

    def addTempData(self, nfcId, temp):
        params = {'nfcId':nfcId, 'temperature':temp}
        response = requests.get(self.URL + '/addTempData', params=params)
        state = response.status_code
        result = response.json()
        print(result)

    def addUser(self, nfcId, name, belong=None):
        params = {'nfcId':nfcId, 'name':name, 'belong' : belong}
        response = requests.get(self.URL + '/addUser', params=params)
        state = response.status_code
        result = response.json()
        return result['result']

    def deleteUser(self, targets):
        targets = ['0'] + targets #add any element to first index of list
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
    # addTempData('12345678', '36.4')
    # print(getNameByNFC('12345678'))
    # addUser('12345678', '홍길동')
    # getUserData()
    # deleteUser(['12039', '12308904', '1234'])
    deleteUser(['12039'])