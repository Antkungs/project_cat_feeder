from datetime import datetime, timedelta
import time
x = 2
while True:
    current_time = datetime.now()
    updated_time = current_time + timedelta(seconds=5)

    print("Current time (hh:mm:ss):", current_time)
    print("updated_time (hh:mm:ss):", updated_time)
    time.sleep(1)