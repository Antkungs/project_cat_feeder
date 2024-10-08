

import time
import board
import busio
import adafruit_vl53l0x
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X
import datetime
import time
import RPi.GPIO as GPIO
import busio
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X

def changePercen(x,y):
    Width = 20
    longs = 10
    cubicVolume = 2600
    x = 12 - 12 if x > 13 else 13 - x
    y = 12 - 12 if y > 13 else 13 - y
    x = (((Width*longs)*x)*100)/cubicVolume
    y = (((Width*longs)*y)*100)/cubicVolume
    return int(x),int(y)

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

while True:
    try:
        x = (((vl53_1.range / 10)-3.5))
        print(x)
        time.sleep(1)
    except Exception as e:
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
