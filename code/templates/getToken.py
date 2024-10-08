import requests
name = ""
# เรียกใช้ API /catinformation
response = requests.get('http://localhost:3000/notification')
if response.status_code == 200:
    cats = response.json()  # รับข้อมูลทั้งหมดจาก API
    # ลูปผ่านทุกตัวแปรตัวแปร cat ในลิสต์ cats
    for cat in cats:
        if cat['id_cat'] == 2:  # เช็คว่า id_cat เป็น 1 หรือไม่
            name = cat['name_cat'] # แปลงเวลาจากข้อความเป็น datetime
else:
    print('Error:', response.text)
