import requests

def getdata(id):#info of cat
    url = 'http://localhost:5000/catinformation/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Failed to fetch data from the API")

