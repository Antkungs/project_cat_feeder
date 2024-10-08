import requests
import datetime

# กำหนดค่าตัวแปร
id_cats = 1
food_give = 110
Food_remaining = 60
Food_eat = food_give - Food_remaining
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# URL สำหรับเซิร์ฟเวอร์
url = 'http://localhost:3000/setEatinformation'

# สร้างข้อมูลในรูปแบบ JSON
data = {
    'ID_Cat': id_cats,
    'food_give': food_give,
    'Food_eat': Food_eat,
    'Food_remaining': Food_remaining,
    'CurrentTime': timestamp
}

# ส่งคำขอ POST
try:
    response = requests.post(url, json=data)  # ใช้ POST แทน GET
    response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับ
    print('Update successful:', response.json())  # แสดงผลลัพธ์
except requests.RequestException as e:
    print('Error:', e)  # แสดงข้อผิดพลาดถ้ามี