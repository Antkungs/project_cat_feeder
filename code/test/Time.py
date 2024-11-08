from datetime import datetime
import time
import requests
import LineNotifi as line
time_data = []

def getTime(select):
    try:
        global haveEat
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # รับข้อมูลทั้งหมดจาก API
            for cat in cats:  # loop เช็ค
                #เช็คไอดีให้ตรงกับค่าที่ส่งมา
                if cat['id_cat'] == select:
                    
                    id_cat = cat['id_cat']
                    name = cat['name_cat']# ดึงชื่อแมว

                    food_give = cat['food_give']#อาหารที่จะให้(กรัม)
                    id_tank = cat['id_tank']#ไอดี tank (Servo select)
                    #เวลามื้อที่ 1,2,3 และ สถานะการกิน
                    time_data = [
                        #มื้อที่ 1
                        {'start': datetime.strptime(cat['time1_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time1_end'], "%H:%M:%S").time(),
                        'status': cat['time1_status']},
                        #มื้อที่ 2
                        {'start': datetime.strptime(cat['time2_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time2_end'], "%H:%M:%S").time(),
                        'status': cat['time2_status']},
                        #มื้อที่ 3
                        {'start': datetime.strptime(cat['time3_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time3_end'], "%H:%M:%S").time(),
                        'status': cat['time3_status']}
                    ]
                    
                    current_time = datetime.now().time() #เวลาปัจจุบัน
                    print(id_cat)
                    print(current_time)
                    ### loop เก็บค่าเวลาและสถานะการกิน idx = มื้อ 
                    for idx, data in enumerate(time_data):
                        start_time = data['start']
                        end_time = data['end']
                        status = data['status']
                    
                        ### เช็คสถานะเวลาและการกินว่ากินไปหรือยัง ถ้ายังให้ทำอะไรก็ได้และตั้งค่าสถานะว่ากินไปแล้ว ###
                        #เวลาต้องอยู่ระหว่าง start and end staus ต้องเป็น false
                        if start_time <= current_time <= end_time and not status :
                            print("current_time pass")
                            #hardwareSelect.giveFood(food_give,id_tank)###process ทำการส่งค่าเพื่อเรียกใช้ Servo hardwareSelect.giveFood(food_give,id_tank) ปริมาณอาหาร,Servo ที่ต้องหมุน ###
                            times = idx + 1
                            print(f"Processed ID {select} for time {times}")
                            #เปลี่ยนสถานะ ณ เวลาที่มีการทำงาน  ให้เป็น True เพื่อป้องกันการทำซ้ำอีกรอบ
                            requests.get(f'http://localhost:3000/setstatus?id={select}&time={times}&status={True}')

                            ### แจ้งเตือนไลน์ ว่าตัวไหนมากิน ###
                            current_time_string = current_time.strftime("%H:%M:%S")
                            line.sendCatEat(name , current_time_string)
                            ### แจ้งเตือนไลน์ ###
                            haveEat = True

                        else:
                            #ไม่มีเวลาการกิน
                            print("not in time")
        else:
            print('Error:', response_cat.text)
            haveEat = False
    except Exception as e:
        print('Error occurred while processing responseCat:', e)
select = 1
haveEat = False
def a():
    try:
        global haveEat
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # Fetch data from API
            cat = next((c for c in cats if c['id_cat'] == select), None)  # Find the right cat by id

            if cat:
                jasonCatInformation = {
                    'idCat': cat['id_cat'],
                    'nameCat': cat['name_cat'],
                    'foodGive': cat['food_give'],
                    'idTank': cat['id_tank']
                }

                # Pre-parse meal times and statuses
                time_data = [
                    {'start': cat['time1_start'], 'end': cat['time1_end'], 'status': cat['time1_status']},
                    {'start': cat['time2_start'], 'end': cat['time2_end'], 'status': cat['time2_status']},
                    {'start': cat['time3_start'], 'end': cat['time3_end'], 'status': cat['time3_status']}
                ]

                current_time = datetime.now().time()  # Get current time
                print(f"ID : {jasonCatInformation['idCat']}\n"
                        f"Name : {jasonCatInformation['nameCat']}\n"
                        f"foodGive : {jasonCatInformation['foodGive']}\n"
                        f"idTank : {jasonCatInformation['idTank']}\n"
                        f"Current Time : {current_time}\n")

                # Loop through time data to check meal schedules
                for idx, data in enumerate(time_data):
                    start_time = datetime.strptime(data['start'], "%H:%M:%S").time()
                    end_time = datetime.strptime(data['end'], "%H:%M:%S").time()
                    status = data['status']

                    # Check if within the eating window and if not already eaten
                    if start_time <= current_time <= end_time and not status:
                        print("current_time pass")
                        
                        # Process food dispensing
                        jasonCatInformation = jasonCatInformation
                        
                        times = idx + 1
                        print(f"Processed ID {select} for time {times}")

                        # Update status to prevent reprocessing
                        update_status_url = f'http://localhost:3000/setstatus?id={select}&time={times}&status={True}'
                        requests.get(update_status_url)

                        # Notify Line
                        current_time_string = current_time.strftime("%H:%M:%S")
                        try:
                            line.sendCatEat(jasonCatInformation['nameCat'], current_time_string)
                        except Exception as e:
                            print("Line Error:", e)

                        haveEat = True
                        return jasonCatInformation
                    else:
                        print("not in time")

                return "nothing"
        else:
            print(f'Error: {response_cat.status_code} - {response_cat.text}')
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

while True:
    a()
    time.sleep(1)