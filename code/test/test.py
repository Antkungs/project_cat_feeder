#current
import datetime
import time

import requests
import LineNotifi as line
from gpiozero import DistanceSensor
def getData():
    try:
        # Make the GET request to the endpoint
        response = requests.get('http://localhost:3000/getPercenTank')
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract 'hour' and 'tanks' from the JSON response
            hour = data.get('hour')
            tanks = data.get('tanks')  # Expecting this to be a list of dictionaries
            
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
    # Get the current time
    now = datetime.datetime.now()
    
    # Check if the current time is exactly '00:01:00' in 24-hour format
    if now.hour == 0 and now.minute == 1:
        return True
    return False

def changePercen(x,y):
    Width = 20
    longs = 10
    cubicVolume = 2200
    x = 12 - 12 if x > 12 else 12 - x
    y = 12 - 12 if y > 12 else 12 - y

    x = (((Width*longs)*x)*100)/cubicVolume
    y = (((Width*longs)*y)*100)/cubicVolume
    return int(x),int(y)

status = {
    'x': False,
    'y': False,
    'z': False
}

boolHourCheck = False
xfuture_time = None
yfuture_time = None
zfuture_time = None
current_time = datetime.datetime.now()
do_time = current_time + datetime.timedelta(seconds=1)

ultrasonic1 = DistanceSensor(echo=27, trigger=22)  # Sensor 1
#ultrasonic2 = DistanceSensor(echo=5, trigger=6)  # Sensor 2
#ultrasonic3 = DistanceSensor(echo=12, trigger=16)
 
#distance2 = ultrasonic2.distance * 100
#distance3 = ultrasonic3.distance * 100
while True:
    current_time = datetime.datetime.now()
    if current_time >= do_time:
        do_time = current_time + datetime.timedelta(seconds=20)
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
        y = 9#ultrasonic2.distance * 100
        z = 5#1ultrasonic3.distance * 100
        print("check")
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
        print("do nothing")

    time.sleep(0.5)