import datetime
import time
import RPi.GPIO as GPIO
import busio
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X
import requests
import LineNotifi as line

# Initialize I2C and GPIO
i2c = busio.I2C(3, 2)
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
time.sleep(0.5)
GPIO.output(14, 0)
GPIO.output(15, 0)
GPIO.output(18, 0)
time.sleep(0.5)

time.sleep(0.5)
GPIO.output(14, 1)
time.sleep(0.5)
vl53_1 = VL53L0X(i2c, address=0x29) #ถัง1
print("ถัง 1 อ่านค่าที่ address 0x29")
vl53_1.set_address(0x2A)
print("ถัง 1 เปลี่ยน address เป็น 0x2A")

time.sleep(0.5)
GPIO.output(15, 1)
time.sleep(0.5)
vl53_2 = VL53L0X(i2c, address=0x29) #ถัง2
print("ถัง 2 อ่านค่าที่ address 0x29")
vl53_2.set_address(0x2B)
print("ถัง 2 เปลี่ยน address เป็น 0x2B")

time.sleep(0.5)
GPIO.output(18, 1)
time.sleep(0.5)
vl53_3 = VL53L0X(i2c, address=0x29) #ถังเศษอาหาร
print("ถัง 3 อ่านค่าที่ address 0x29")
vl53_3.set_address(0x2C)
print("ถัง 3 เปลี่ยน address เป็น 0x2C")

time.sleep(0.5)
vl53_1.measurement_timing_budget = 100000
vl53_2.measurement_timing_budget = 100000
vl53_3.measurement_timing_budget = 100000

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
         
def convert_z(value):
    try:
        max_cm = 29
        min_cm = 19
        if value >= max_cm:
            value = 29
        elif value <= min_cm:
            value = 19
        return (((value-max_cm)/(min_cm-max_cm))*100)*-1
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def changePercen(x,y):
    Width = 20
    longs = 10
    cubicVolume = 2600
    x = 13 - 13 if x > 13 else 13 - x
    y = 13 - 13 if y > 13 else 13 - y
    x = (((Width*longs)*x)*100)/cubicVolume
    y = (((Width*longs)*y)*100)/cubicVolume
    return int(x),int(y)


def is_000100():
    now = datetime.datetime.now()
    
    # Check if the current time is exactly '00:01:00' in 24-hour format
    if now.hour == 0 and now.minute == 1:
        return True
    return False


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
        #input sensor
        xcm = (vl53_1.range / 10) -3.5
        ycm = (vl53_2.range / 10)
        zcm = (vl53_3.range / 10) - 3
        print("\n\ncheck\n")
        # % เมื่อต้องกาารแจ้งเตือน get api
        Notification = {
        'x' : tank[0]['notification_percen'],
        'y' : tank[1]['notification_percen'],
        'z' : 80
        }
        x , y = changePercen(xcm,ycm)
        z = convert_z(zcm)
        current_time = datetime.datetime.now()
        print(f"x {x} % : Notification {Notification['x']} %\ny {y} % : Notification {Notification['y']} %\nz {z} % : Notification {Notification['z']} %")
        print(f"{hour} hour")

        if x > Notification['x']:
            status['x'] = False
            xfuture_time = None
        if x <= Notification['x']:
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
            #api.resetStatusToFalse()

        #print("do nothing")

    time.sleep(0.5)
