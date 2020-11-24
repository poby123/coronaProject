import requests
import json
import time
from multiprocessing import Value


class DataController():

    def __init__(self, interrupt=None):
        self.URL = 'https://ssu-corona.herokuapp.com'
        # self.URL = 'http://localhost:3000'
        if(interrupt != None):
            self.interrupt = interrupt

    def getUserDataByNFC(self, nfcid):
        params = {'nfcid': nfcid}
        response = requests.get(
            self.URL + '/rest/user/identify', params=params)
        state = response.status_code
        result = response.json()
        if(result['result'] == True):
            return result['obj']
        else:
            return None

    def addTempData(self, nfcid, temp):
        params = {'nfcid': nfcid, 'temperature': temp}
        response = requests.get(self.URL + '/rest/addTempData', params=params)
        state = response.status_code
        result = response.json()
        print(result)

    def addUser(self, nfcid, name, belong, id):
        data = {'target': {'nfcid': nfcid,
                           'name': name, 'belong': belong, 'id': id}}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(
            self.URL + '/rest/user', headers=headers, data=json.dumps(data))
        state = response.status_code
        result = response.json()
        return result['result']

    def deleteUser(self, targets):
        data = {'target': targets}
        response = requests.delete(self.URL + '/rest/user', data=data)
        result = response.json()
        return result['result']

    def getUserData(self):
        time.sleep(1)
        response = requests.get(self.URL + '/rest/user/withouttemp')
        state = response.status_code
        result = response.json()
        if(result['result'] == True):
            return result['content']
        else:
            return None

    def login(self, id, password):
        data = {'id': id, 'password': password}
        # headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(
            self.URL + '/auth/signin', data=data)
        state = response.status_code
        result = response.json()
        return result['flag']

    def logout(self):
        requests.get(self.URL + '/auth/signout')


if __name__ == '__main__':
    dc = DataController()
    # print(dc.addUser('12345678', '이름 테스트', '소속 테스트'))
    # print(dc.getUserDataByNFC(1234))
    # print(dc.login('admin', 'adminpassword'))
    # dc.logout()
    print(dc.getUserData())
    # print(dc.deleteUser(659519540980))
