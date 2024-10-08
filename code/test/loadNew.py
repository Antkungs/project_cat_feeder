import time
import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice
from hx711 import HX711

# Define GPIO pins
DT = 5  # GPIO pin for data
SCK = 6  # GPIO pin for clock

hx = HX711(DT, SCK)
servo_pwm = PWMOutputDevice(12)

# Setup function
def setup():
    # hx.set_reading_format("MSB", "MSB")  # Commented out
    hx.set_reference_unit(685)  # Use the calculated reference unit
    hx.reset()
    hx.tare()  # Perform tare

# Function to read weight
def read_weight():
    weight = hx.get_weight(5)  # Read average weight 5 times
    return weight

# Initialize setup
setup()
try:
    while True:
        # for i in range(10):  # Loop 10 times
            weight = read_weight()  # Read weight
            print(f"Weight: {weight:.2f} g")  # Display weight in grams
            time.sleep(1)  # Wait 1 second

        # Control servo after reading weight
        # print("Servo moving...")
        # servo_pwm.value = 0.05  # Set servo to first position
        # time.sleep(1)
        # servo_pwm.value = 0.16  # Set servo to second position
        # time.sleep(3)
        # servo_pwm.value = 0.05  # Return servo to first position
        # time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    GPIO.cleanup()
