#request package document : https://requests.readthedocs.io/en/master/user/quickstart/
import requests #pip install requests 명령을 통해 설치한다.

URL = 'http://www.tistory.com'
response = requests.get(URL)
# print(response.status_code)
# print(response.text)

a = []
a.append({"window":3, "ui" : 4})
a.append({"window":3, "ui" : 5})
a.append({"window":3, "ui" : 6})
print(a[0]["window"])
