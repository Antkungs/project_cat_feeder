import requests
select = 0
name = ""
food_give = ""
id_tank = ""
time1_start = ""
time1_end = ""
time2_start = ""
time2_end = ""
time3_start = ""
time3_end = ""
time1_status = ""
time2_status = ""
time3_status = ""
time_ranges = []
token = ""
hour = ""

# เรียกใช้ API /catinformation
def getSelect(id):
    return id
select = getSelect(2)

responseCat = requests.get('http://localhost:3000/catinformation')
responseToken = requests.get('http://localhost:3000/notification')
try:
    if responseCat.status_code == 200:
        cats = responseCat.json()  # รับข้อมูลทั้งหมดจาก API
        # ลูปผ่านทุกตัวแปรตัวแปร cat ในลิสต์ cats
        for cat in cats:
            if cat['id_cat'] == select:
                print(cat['id_cat'])  # เช็คว่า id_cat เป็น 1 หรือไม่
                name = cat['name_cat']
                food_give = cat['food_give']
                id_tank = cat['id_tank']
                time1_start = cat['time1_start']
                time1_end = cat['time1_end']
                time2_start = cat['time2_start']
                time2_end = cat['time2_end']
                time3_start = cat['time3_start']
                time3_end = cat['time3_end']
                time1_status = cat['time1_status']
                time2_status = cat['time2_status']
                time3_status = cat['time3_status']
                time_ranges.append((
                    time1_start, time1_end,
                    time2_start, time2_end,
                    time3_start, time3_end,
                ))
    else:
        print('Error:', responseCat.text)
except Exception as e:
    print('Error occurred while processing responseCat:', e)

try:
    if responseToken.status_code == 200:  
        datas = responseToken.json()
        for data in datas:
            token = data['token']
            hour = data['hour']
    else:
        print('Error:', responseToken.text)
except Exception as e:
    print('Error occurred while processing responseToken:', e)


