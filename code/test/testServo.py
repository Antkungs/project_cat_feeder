from gpiozero import OutputDevice,PWMOutputDevice,Button
from time import sleep
try:
    led3 = OutputDevice(17)
    led3.off()
    servo_pwm = PWMOutputDevice(12)
    led3.on()
    servo_pwm.value = 0.05
    sleep(1)
    servo_pwm.value = 0.16
    sleep(0.5)
    # servo_pwm.value = 0.13
    # sleep(0.5)
    # servo_pwm.value = 0.16
    # sleep(0.5)
    # servo_pwm.value = 0.13
    # sleep(1)
    servo_pwm.value = 0.05
    sleep(1)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    led3.off()
    servo_pwm.close()
    led3.close()
    print("Servo Ending")