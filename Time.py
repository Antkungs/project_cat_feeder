from datetime import datetime
import time
import requests
import LineNotifi as line
time_data = []

def getTime(select):
    try:
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            # รับข้อมูลทั้งหมดจาก API
            cats = response_cat.json()  # รับข้อมูลทั้งหมดจาก API
            for cat in cats:
                current_time = datetime.now().time()
                if cat['id_cat'] == select:
                    name = cat['name_cat']
                    food_give = cat['food_give']
                    id_tank = cat['id_tank']
                    #เวลาที่ 1,2,3 และ สถานะ
                    time_data = [
                        {'start': datetime.strptime(cat['time1_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time1_end'], "%H:%M:%S").time(),
                        'status': cat['time1_status']},

                        {'start': datetime.strptime(cat['time2_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time2_end'], "%H:%M:%S").time(),
                        'status': cat['time2_status']},

                        {'start': datetime.strptime(cat['time3_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time3_end'], "%H:%M:%S").time(),
                        'status': cat['time3_status']}
                    ]
                    ### loop เก็บค่าเวลาและสถานะการกิน
                    for idx, data in enumerate(time_data):
                        start_time = data['start']
                        end_time = data['end']
                        status = data['status']

                        print(current_time)
                        ### เช็คสถานะเวลาและการกินว่ากินไปหรือยัง ถ้ายังให้ทำอะไรก็ได้และตั้งค่าสถานะว่ากินไปแล้ว ###
                        if start_time <= current_time <= end_time and not status:
                            print("here")
                            ### process more ###
                            times = idx + 1
                            print(f"Processed ID {select} for time {times}")
                            requests.get(f'http://localhost:3000/setstatus?id={select}&time={times}&status={True}')

                            ### แจ้งเตือนไลน์ ###
                            responseToken = requests.get('http://localhost:3000/notification')
                            try:
                                if responseToken.status_code == 200:  
                                    datas = responseToken.json()
                                    for data in datas:
                                        token = data['token']
                                else:
                                    print('Error:', responseToken.text)
                            except Exception as e:
                                print('Error occurred while processing responseToken:', e)

                            line.sendCatEat(token, name)
                            ### แจ้งเตือนไลน์ ###

                        else:
                            print("none")
        else:
            print('Error:', response_cat.text)
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

while True:
    getTime(2)
    time.sleep(5)
    getTime(1)