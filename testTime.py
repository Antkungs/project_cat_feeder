import time
import datetime

# รับค่าเวลาปัจจุบันในหน่วยวินาที
while True:
    x = input("Enter 'reset' to reset the second or any other key to stop: ")
    if x.lower() == 'reset':
        timestamp = time.time()

        # แปลง timestamp เป็น datetime object
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)

        second = datetime_obj.second
        print("Current second:", second)
    else:
        print("Stop")
        break
