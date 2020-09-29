import requests

URL = 'http://localhost:3000/rest' 
# # response = requests.get(URL+'/identify?nfcId=12345678')
# # response = requests.get(URL + '/deleteUser?nfcId=12345678')
# print(response.status_code )
# print(response.text)

def getNameByNFC(nfcId):
    params = {'nfcId':nfcId}
    response = requests.get(URL + '/identify', params=params)
    state = response.status_code
    result = response.json()
    print(result)

def addTempData(nfcId, temp):
    params = {'nfcId':nfcId, 'temperature':temp}
    response = requests.get(URL + '/addTempData', params=params)
    state = response.status_code
    result = response.json()
    print(result)

def addUser(nfcId, name):
    params = {'nfcId':nfcId, 'name':name}
    response = requests.get(URL + '/addUser', params=params)
    state = response.status_code
    result = response.json()
    print(result)

def getUserData():
    response = requests.get(URL + '/userInfoWithoutTemp')
    state = response.status_code
    result = response.json()
    print(result)
    print(result['content'])

if __name__ == '__main__':
    # addTempData('12345678', '36.4')
    # getNameByNFC('12345678')
    # addUser('12345678', '홍길동')
    getUserData()