from gpiozero import OutputDevice,PWMOutputDevice,Button, DistanceSensor
from time import sleep
switch1 = Button(20, bounce_time=0.1) 
switch2 = Button(21, bounce_time=0.1) 
switch3 = Button(26, bounce_time=0.1) 
while True:
    print(switch1)
    print(switch2)
    print(switch3)
    sleep(1)