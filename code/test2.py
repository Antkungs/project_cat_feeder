import time
import RPi.GPIO as GPIO
import board
import busio
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X

# Initialize I2C and GPIO
i2c = busio.I2C(3, 2)
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output(14, 1)
GPIO.output(15, 0)
GPIO.output(18, 0)
time.sleep(0.5)

# Initialize sensors
#print("1")
#GPIO.output(14, 1)
#time.sleep(0.5)
#vl53_1 = VL53L0X(i2c, address=0x29) #ถัง1
print("2")
#GPIO.output(15, 1)
#time.sleep(0.5)
#vl53_2 = VL53L0X(i2c, address=0x2A) #ถัง2
print("3")
#GPIO.output(18, 1)
#time.sleep(0.5)
#vl53_3 = VL53L0X(i2c, address=0x2B) #ถังเศษอาหาร
print("4")
time.sleep(0.5)

# Set measurement timing budget
#vl53_1.measurement_timing_budget = 200000
#vl53_2.measurement_timing_budget = 200000
#vl53_3.measurement_timing_budget = 200000
###
# Function to change percentage
def changePercen(x, y):
    Width = 20
    longs = 10
    cubicVolume = 2600
    x = 13 - 13 if x > 13 else 13 - x
    y = 13 - 13 if y > 13 else 13 - y
    x = (((Width * longs) * x) * 100) / cubicVolume
    y = (((Width * longs) * y) * 100) / cubicVolume
    return int(x), int(y)

# Main loop
time.sleep(5)
for _ in range(10):
    try:
        # Attempt to read distances from the sensors
         try:
             x = (vl53_1.range / 10) - 3.5
             print("ทดสอบ3ซม")
             print("Range1: {0}cm".format(x))
         except Exception as e:
             print("Error reading Range1: ", e)

         #try:
             #y = (vl53_2.range / 10) - 2.7
             #print("senser2")
             #print("Range2: {0}cm".format(y))
         #except Exception as e:
             #print("Error reading Range2: ", e)

        #try:
            #print("Senser3")
            #z = (vl53_3.range / 10) - 2.5
            #print("Range3: {0}cm".format(z))
        #except Exception as e:
            #print("Error reading Range3: ", e)

         print("===================================================")
         time.sleep(0.5)


    except KeyboardInterrupt:
        print("Exiting...")
        break

