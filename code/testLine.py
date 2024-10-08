import datetime
import LineNotifi as li
current_time =  datetime.time() 
current_time_string = current_time.strftime("%H:%M:%S")
li.sendTankFull()
li.sendCatEat(1,current_time_string)
li.sendTankLow(1)
