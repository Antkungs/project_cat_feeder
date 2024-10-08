from gpiozero import OutputDevice,PWMOutputDevice,Button
from time import sleep
led1 = OutputDevice(22)
led1.off()
def switchOnPlace1():
    led1.on()
    sleep(1)
    led1.off()
    sleep(1)
while True:
    led1.on()
    sleep(1)
    led1.off()
    sleep(1)
