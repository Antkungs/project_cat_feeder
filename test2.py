import Time
import api
import time
import LineNotifi as li
li.sendTankFull()
li.start()
li.sendTankLow(1)
li.sendCatEat("cat1","12:00:00")
li.send_text("hello")
