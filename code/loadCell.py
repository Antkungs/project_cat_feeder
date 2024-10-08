import RPi.GPIO as GPIO
from hx711 import HX711

def setup():
    GPIO.setmode(GPIO.BCM)
    return HX711(dout_pin=5, pd_sck_pin=6)

def tare_scale(hx):
    if hx.zero():
        raise ValueError('Tare is unsuccessful.')

def calibrate_scale(hx):
    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    known_weight_grams = float(input('Write how many grams it was and press Enter: '))
    ratio = reading / known_weight_grams
    hx.set_scale_ratio(ratio)
    print('Ratio is set.')

def read_weight(hx):
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    while True:
        print(hx.get_weight_mean(20), 'g')

if __name__ == "__main__":
    try:
        hx = setup()
        tare_scale(hx)
        calibrate_scale(hx)
        read_weight(hx)
    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')
    finally:
        GPIO.cleanup()
