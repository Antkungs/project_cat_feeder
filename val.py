import requests
import LineNotifi as line
name = "hello"
responseToken = requests.get('http://localhost:3000/notification')
try:
    if responseToken.status_code == 200:  
        datas = responseToken.json()
        for data in datas:
            token = data['token']
        line.sendCatEat(token, name)
    else:
        print('Error:', responseToken.text)
except Exception as e:
    print('Error occurred while processing responseToken:', e)