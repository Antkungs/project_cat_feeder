import RPi.GPIO as GPIO
import time

# ตั้งค่าโหมดการทำงานของ GPIO
GPIO.setmode(GPIO.BCM)

# กำหนด pin ที่ใช้กับสวิตช์
switch_1_pin = 20
switch_2_pin = 21
switch_3_pin = 26

# ตั้งค่า pin เป็น input และเปิด pull-up resistor
GPIO.setup(switch_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # อ่านค่าสัญญาณจากสวิตช์แต่ละตัว
        switch_1_state = GPIO.input(switch_1_pin)
        switch_2_state = GPIO.input(switch_2_pin)
        switch_3_state = GPIO.input(switch_3_pin)

        # ตรวจสอบสถานะของสวิตช์ 1
        if switch_1_state == GPIO.LOW:
            print("Switch 1 Pressed")
        else:
            print("Switch 1 Released")
        
        # ตรวจสอบสถานะของสวิตช์ 2
        if switch_2_state == GPIO.LOW:
            print("Switch 2 Pressed")
        else:
            print("Switch 2 Released")

        # ตรวจสอบสถานะของสวิตช์ 3
        if switch_3_state == GPIO.LOW:
            print("Switch 3 Pressed")
        else:
            print("Switch 3 Released")

        time.sleep(0.8)

        print("=================================")

except KeyboardInterrupt:
    pass

finally:
    # ทำความสะอาดการตั้งค่า GPIO
    GPIO.cleanup()
