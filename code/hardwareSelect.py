from gpiozero import OutputDevice,PWMOutputDevice,Button, DistanceSensor
from time import sleep
import requests
import datetime
import serial
import serial.tools.list_ports
import LineNotifi as line
import time
import api

led1 = OutputDevice(22)
led1.off()
led2 = OutputDevice(27)
led2.off()

def found_comport():
    global ser_obj
    # List available serial ports
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return
    # Print all available ports
    for port in ports:
        print(f"Found port: {port.device}")
    # Choose the first available port
    if ports:
        port_name = ports[0].device  # Use the first available port
        try:
            # Attempt to open the serial port
            ser = serial.Serial(port_name, 9600, timeout=1)
            if ser.is_open:
                print(f"Serial port {ser.portstr} is open")
                ser_obj = ser
        except serial.SerialException as e:
            print(f"Error opening serial port {port_name}: {e}")
            ser_obj = None
    # รอให้ Serial Port เริ่มต้น
    time.sleep(1)

def switchOnPlace1():
    try:
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # รับข้อมูลทั้งหมดจาก API
            for cat in cats:  # loop เช็ค
                #เช็คไอดีให้ตรงกับค่าที่ส่งมา
                if cat['id_cat'] == 1:
                    id_cat = 1
                    name = cat['name_cat']# ดึงชื่อแมว

                    food_give = cat['food_give']#อาหารที่จะให้(กรัม)
                    id_tank = cat['id_tank']#ไอดี tank (Servo select)
                    #เวลามื้อที่ 1,2,3 และ สถานะการกิน
                    jasonCatInformation = {
                        'idCat': id_cat,
                        'nameCat': name,
                        'foodGive': food_give,
                        'idTank': id_tank
                    }
        print(jasonCatInformation)
        swLoadCell(jasonCatInformation)
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

def switchOnPlace2():
    try:

        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # รับข้อมูลทั้งหมดจาก API
            for cat in cats:  # loop เช็ค
                #เช็คไอดีให้ตรงกับค่าที่ส่งมา
                if cat['id_cat'] == 2:
                    id_cat =  2
                    name = cat['name_cat']# ดึงชื่อแมว

                    food_give = cat['food_give']#อาหารที่จะให้(กรัม)
                    id_tank = cat['id_tank']#ไอดี tank (Servo select)
                    #เวลามื้อที่ 1,2,3 และ สถานะการกิน
                    jasonCatInformation = {
                        'idCat': id_cat,
                        'nameCat': name,
                        'foodGive': food_give,
                        'idTank': id_tank
                    }
        print(jasonCatInformation)
        swLoadCell(jasonCatInformation)
    except Exception as e:
        print('Error occurred whie processing responseCat:', e)
    
def switchOnPlace3():
    try:
        api.servoFood()
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

switch1 = Button(20, bounce_time=0.1) 
switch1.when_released  = switchOnPlace1
switch2 = Button(21, bounce_time=0.1) 
switch2.when_released  = switchOnPlace2
switch3 = Button(26, bounce_time=0.1) 
switch3.when_released  = switchOnPlace3

def convert_to_float(data_str):
    try:
        if data_str is None or data_str == '':
            return 0.0
        # Convert the string to a float
        return float(data_str)
    except ValueError:
        # Handle the case where conversion fails
        print(f"Error converting '{data_str}' to float.")
        return None

def loadRange(select_value,range_value):
    try:
        servo_pwm = PWMOutputDevice(12)
        servo_pwm.value = 0.05
        sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        servo_pwm.close()
        print("Servo Ending")
    try:        
        motor1 = PWMOutputDevice(23)
        motor2 = PWMOutputDevice(24)
        found_comport()
        current_time = time.time()
        end_time = current_time + 60
        if ser_obj:
            ser = ser_obj
            food_give = range_value
            id_tank = select_value
            try:
                motor_map = {
                '1': motor1,
                '2': motor2,
                }

                led_select = {
                "1" : led1,
                "2" : led2,
                }

                device_name = f"{id_tank}"
                device = motor_map.get(device_name)

                led_name = f"{id_tank}"
                leds = led_select.get(led_name)
                food_give = convert_to_float(food_give)
                while True:
                    if ser.in_waiting > 0:
                        data = ser.readline().decode('utf-8').rstrip()
                        number = convert_to_float(data)
                        print(number)
                        if number is not None:
                            leds.on()
                            print("motor run")
                            current_time = time.time()
                            if current_time >= end_time:
                                leds.off()
                                device.value = 0
                                print("motor stop")
                                break
                            elif number >= food_give * 0.97:
                                leds.off()
                                device.value = 0
                                print("motor stop")
                                break
                            elif  food_give < 20:
                                device.value = 0.35
                            elif number > food_give * 0.8:
                                device.value = 0.4
                                print("food is > 80%")
                            elif number > food_give * 0.65:
                                device.value = 0.6
                                print("food > 65%")
                            elif number > 0:
                                device.value = 0.7

                        else:
                            print("wait")
                            current_time = time.time()
                            if current_time >= end_time:
                                break


            except KeyboardInterrupt:
                print("Program interrupted.")
            finally:
                if ser and ser.is_open:
                    motor1.close()
                    motor2.close()
                    ser.close()
                print("Serial connection closed.")
    except Exception as e:
        print("Error occurred while reading from serial port:", e)

def swLoadCell(jasonCatInformation):
    try:
        servo_pwm = PWMOutputDevice(12)
        servo_pwm.value = 0.05
        sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        servo_pwm.close()
        print("Servo Ending")
    try:
        motor1 = PWMOutputDevice(23)
        motor2 = PWMOutputDevice(24)
        found_comport()
        current_time = time.time()
        end_time = current_time + 60
        if ser_obj:
            ser = ser_obj
            id_cats = jasonCatInformation["idCat"]
            names = jasonCatInformation["nameCat"]
            food_give = jasonCatInformation["foodGive"]
            id_tank = jasonCatInformation["idTank"]
            try:
                motor_map = {
                '1': motor1,
                '2': motor2,
                }

                led_select = {
                "1" : led1,
                "2" : led2,
                }

                device_name = f"{id_tank}"
                device = motor_map.get(device_name)

                led_name = f"{id_tank}"
                leds = led_select.get(led_name)
                food_give = convert_to_float(food_give)
                while True:
                    if ser.in_waiting > 0:

                        data = ser.readline().decode('utf-8').rstrip()
                        number = convert_to_float(data)
                        print(number)
                        if number is not None:
                            leds.on()
                            print("motor run")
                            current_time = time.time()
                            if current_time >= end_time:
                                leds.off()
                                jasonCatInformation = {
                                    'idCat': id_cats,
                                    'nameCat': names,
                                    'foodGive': number,
                                    'idTank': id_tank
                                }
                                break
                            elif number >= food_give * 0.97:
                                device.value = 0
                                data = ser.readline().decode('utf-8').rstrip()
                                number = convert_to_float(data) 
                                current_time = time.time()
                                breakLoad = current_time + 2 
                                print("motor stop")
                                while True:
                                    current_time = time.time()
                                    print(number)
                                    if current_time >= breakLoad:
                                        leds.off()
                                        jasonCatInformation = {
                                            'idCat': id_cats,
                                            'nameCat': names,
                                            'foodGive': number,
                                            'idTank': id_tank
                                        }
                                        break
                                break
                            elif  food_give < 20:
                                device.value = 0.35
                            elif number > food_give * 0.8:
                                device.value = 0.4
                                print("food is > 80%")
                            elif number > food_give * 0.65:
                                device.value = 0.6
                                print("food > 65%")
                            elif number > 0:
                                device.value = 0.7

                        else:
                            print("wait")
                            current_time = time.time()
                            if current_time >= end_time:
                                break


            except KeyboardInterrupt:
                print("Program interrupted.")
            finally:
                if ser and ser.is_open:
                    motor1.close()
                    motor2.close()
                    ser.close()
    except Exception as e:
        print("Error occurred while reading from serial port:", e)
        
def loadCell(jasonCatInformation):
    try:
        servo_pwm = PWMOutputDevice(12)
        servo_pwm.value = 0.05
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        servo_pwm.close()
        print("Servo Ending")
    try:
        motor1 = PWMOutputDevice(23)
        motor2 = PWMOutputDevice(24)
        current_time = time.time()
        end_time = current_time + 30
        found_comport()
        if ser_obj:
            print("start")
            ser = ser_obj
            id_cats = jasonCatInformation["idCat"]
            names = jasonCatInformation["nameCat"]
            food_give = jasonCatInformation["foodGive"]
            id_tank = jasonCatInformation["idTank"]
            
            try:
                motor_map = {
                '1': motor1,
                '2': motor2,
                }

                led_select = {
                "1" : led1,
                "2" : led2,
                }

                device_name = f"{id_tank}"
                device = motor_map.get(device_name)

                led_name = f"{id_tank}"
                leds = led_select.get(led_name)
                data = ser.readline().decode('utf-8').rstrip()
                number = convert_to_float(data)
                time.sleep(3) 
                while True:
                    if ser.in_waiting > 0:
                        data = ser.readline().decode('utf-8').rstrip()
                        number = convert_to_float(data)
                        print(number)
                        if number is not None:
                            leds.on()
                            print("motor run")
                            current_time = time.time()
                            if current_time >= end_time:
                                leds.off()
                                jasonCatInformation = {
                                    'idCat': id_cats,
                                    'nameCat': names,
                                    'foodGive': number,
                                    'idTank': id_tank
                                }
                                break
                            elif number >= food_give * 0.97:
                                device.value = 0
                                data = ser.readline().decode('utf-8').rstrip()
                                number = convert_to_float(data) 
                                current_time = time.time()
                                breakLoad = current_time + 2 
                                print("motor stop")
                                while True:
                                    current_time = time.time()
                                    print(number)
                                    if current_time >= breakLoad:
                                        leds.off()
                                        jasonCatInformation = {
                                            'idCat': id_cats,
                                            'nameCat': names,
                                            'foodGive': number,
                                            'idTank': id_tank
                                        }
                                        break
                                break
                            elif  food_give < 20:
                                device.value = 0.35
                            elif number > food_give * 0.8:
                                device.value = 0.4
                                print("food is > 80%")
                            elif number > food_give * 0.65:
                                device.value = 0.6
                                print("food > 65%")
                            elif number > 0:
                                device.value = 0.7

                        else:
                            print("wait")
                            current_time = time.time()
                            if current_time >= end_time:
                                break

            except KeyboardInterrupt:
                print("Program interrupted.")
            finally:
                motor1.close()
                motor2.close()
                if ser and ser.is_open:
                    print("ser close")
                    #ser.close()
                return jasonCatInformation
    except Exception as e:
        print(f"An error occurred: {e}")


def loadFoodEnd(jasonCatInformation):   
    try:
        found_comport()
        if ser_obj:
            ser = ser_obj
            id_cats = jasonCatInformation["idCat"]
            food_give = jasonCatInformation["foodGive"]
            current_time = time.time()
            play_loop_time = current_time + 5
            try:
                while True:
                    if ser.in_waiting > 0:
                        # Read and decode data from the serial port
                        data = ser.readline().decode('utf-8').rstrip()                 
                        number = convert_to_float(data)
                        if number is not None:
                            Food_remaining = number  # Use the float value directly
                            print(Food_remaining)
                            current_time = time.time()
                            if current_time >= play_loop_time:
                                Food_eat = food_give - Food_remaining
                                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                break
                        else:
                            play_loop_time = current_time + 5
                    time.sleep(0.1)  # Sleep to avoid high CPU usage

            except KeyboardInterrupt:
                print("Program interrupted.")
    except Exception as e:
        print("Error occurred while reading from serial port:", e)

    try:
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
        print(data)
        # ส่งคำขอ POST
        try:
            response = requests.post(url, json=data)  # ใช้ POST แทน GET
            response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับ
            print('Update successful:', response.json())  # แสดงผลลัพธ์
        except requests.RequestException as e:
            print('Error:', e)  # แสดงข้อผิดพลาดถ้ามี
                    
    except requests.RequestException as e:
        print('Error occurred while processing responseCat:', e)
    except serial.SerialException as e:
        print('Serial port error:', e)
    finally:
        if ser and ser.is_open:
            ser.close()
        print("Serial connection closed.")

def getData():
    try:
        response = requests.get('http://localhost:3000/getPercenTank')

        if response.status_code == 200:
            data = response.json()
            
            hour = data.get('hour')
            tanks = data.get('tanks')
            
            if hour is not None and tanks is not None:
                return hour, tanks
            else:
                print('Error: "hour" or "tanks" key not found in response')
        else:
            print('Error:', response.text)
    except requests.exceptions.RequestException as e:
        print('Error occurred while making request:', e)
    except Exception as e:
        print('Error occurred while processing response:', e)

def is_000100():
    now = datetime.datetime.now()
    
    # Check if the current time is exactly '00:01:00' in 24-hour format
    if now.hour == 0 and now.minute == 1:
        return True
    return False

def changePercen(x,y):
    Width = 20
    longs = 10
    cubicVolume = 2600
    x = 13 - 13 if x > 13 else 13 - x
    y = 13 - 13 if y > 13 else 13 - y
    x = (((Width*longs)*x)*100)/cubicVolume
    y = (((Width*longs)*y)*100)/cubicVolume
    return int(x),int(y)

def mainHw():
    
    ultrasonic1 = DistanceSensor(echo=27, trigger=22)  # Sensor 1
    #ultrasonic2 = DistanceSensor(echo=5, trigger=6)  # Sensor 2
    #ultrasonic3 = DistanceSensor(echo=12, trigger=16)
    status = {
        'x': False,
        'y': False,
        'z': False
    }

    xfuture_time = None
    yfuture_time = None
    zfuture_time = None
    boolHourCheck = False
    current_time = datetime.datetime.now()
    do_time = current_time + datetime.timedelta(seconds=15)

    while True:
        current_time = datetime.datetime.now()
        if current_time >= do_time:
            do_time = current_time + datetime.timedelta(seconds=30)
            hour , tank = getData()
            hour = hour[0]
            if  boolHourCheck == False:
                hourCheck = hour
                boolHourCheck = True
            if hourCheck != hour:
                print("Change Time")
                boolHourCheck = False
                if xfuture_time != None:
                    xfuture_time = current_time + timeLoop
                    print("Change x")
                if yfuture_time != None:
                    yfuture_time = current_time + timeLoop
                    print("Change y")
                if zfuture_time != None:
                    zfuture_time = current_time + timeLoop
                    print("Change z")
            sec = hour * 60 * 60
            timeLoop = datetime.timedelta(seconds=sec)
            #inout sensor ultrasonic
            x = ultrasonic1.distance * 100 
            y = 9 #ultrasonic2.distance * 100
            z = 5 #1ultrasonic3.distance * 100
            print("\n\ncheck\n")
            print(f"x {x} Cm\ny {y} Cm")
            # % เมื่อต้องกาารแจ้งเตือน get api
            Notification = {
            'x' : tank[0]['notification_percen'],
            'y' : tank[1]['notification_percen'],
            'z' : 85
            }
            x , y = changePercen(x,y)
            current_time = datetime.datetime.now()
            print(f"x {x} % : Notification {Notification['x']} %\ny {y} % : Notification {Notification['y']} %")
            print(f"{hour} hour")

            if Notification['x'] < x:
                status['x'] = False
                xfuture_time = None
            if Notification['x'] >= x:
                if Notification['x'] >= x and status['x'] == False:
                    status['x'] = True
                    current_time = datetime.datetime.now()
                    xfuture_time = current_time + timeLoop
                    print(f"X Notification")
                    line.sendTankLow(1)
                elif current_time >= xfuture_time:
                    print("X Notification Again")
                    line.sendTankLow(1)
                    xfuture_time = current_time + timeLoop

            if Notification['y'] < y:
                status['y'] = False
                yfuture_time = None
            if Notification['y'] >= y:
                if Notification['y'] >= y and status['y'] == False:
                    status['y'] = True
                    current_time = datetime.datetime.now()
                    yfuture_time = current_time + timeLoop
                    print(f"Y Notification")
                    line.sendTankLow(2)
                elif current_time >= yfuture_time:
                    print("Y Notification Again")
                    line.sendTankLow(2)
                    yfuture_time = current_time + timeLoop

            if Notification['z'] > z:
                status['z'] = False
                zfuture_time = None
            if Notification['z'] <= z:
                if Notification['z'] <= z and status['z'] == False:
                    status['z'] = True
                    current_time = datetime.datetime.now()
                    zfuture_time = current_time + timeLoop
                    print(f"Z Notification")
                    line.sendTankFull()
                elif current_time >= zfuture_time:
                    print("Z Notification Again")
                    line.sendTankFull()
                    zfuture_time = current_time + timeLoop
        else:
            if is_000100():
                print("reset time")
                api.resetStatusToFalse()

            #print("do nothing")

        time.sleep(0.5)
"""
def cleanup():
    # Properly close GPIO resources
    led1.close()
    led2.close()
    led3.close()
    motor1.close()
    motor2.close()
    servo_pwm.close()
    switch1.close()
    switch2.close()
    switch3.close()
    print("GPIO resources cleaned up.")
"""
