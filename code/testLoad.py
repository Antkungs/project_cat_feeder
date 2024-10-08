import datetime
import time
import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice , OutputDevice
import serial
import serial.tools.list_ports
from hx711 import HX711
import requests

led1 = OutputDevice(22)
led1.off()
led2 = OutputDevice(27)
led2.off()

def found_comport():
    global ser_obj
    # List available serial ports
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("No serial ports found.")
        return
    
    # Print all available ports
    for port in ports:
        print(f"Found port: {port.device}")
    
    # Choose the first available port
    if ports:
        port_name = ports[0].device  # Use the first available port
        try:
            # Attempt to open the serial port
            ser = serial.Serial(port_name, 9600, timeout=1)
            if ser.is_open:
                print(f"Serial port {ser.portstr} is open")
                ser_obj = ser
        except serial.SerialException as e:
            print(f"Error opening serial port {port_name}: {e}")
            ser_obj = None
    time.sleep(1)

def convert_to_float(data_str):
    try:
        if data_str is None or data_str.strip() == '':
            return 0.0
        return float(data_str)
    except ValueError:
        print(f"Error converting '{data_str}' to float.")
        return None

def loadCell(jasonCatInformation):
    try:
        servo_pwm = PWMOutputDevice(12)
        servo_pwm.value = 0.05
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        servo_pwm.close()
        print("Servo Ending")
    try:
        motor1 = PWMOutputDevice(23)
        motor2 = PWMOutputDevice(24)
        current_time = time.time()
        end_time = current_time + 30
        found_comport()
        if ser_obj:
            print("start")
            ser = ser_obj
            id_cats = jasonCatInformation["idCat"]
            names = jasonCatInformation["nameCat"]
            food_give = jasonCatInformation["foodGive"]
            id_tank = jasonCatInformation["idTank"]
            
            try:
                motor_map = {
                '1': motor1,
                '2': motor2,
                }

                led_select = {
                "1" : led1,
                "2" : led2,
                }

                device_name = f"{id_tank}"
                device = motor_map.get(device_name)

                led_name = f"{id_tank}"
                leds = led_select.get(led_name)
                data = ser.readline().decode('utf-8').rstrip()
                number = convert_to_float(data)
                while True:
                    if ser.in_waiting > 0:
                        data = ser.readline().decode('utf-8').rstrip()
                        number = convert_to_float(data)
                        print(number)
                        if number is not None:
                            leds.on()
                            print("motor run")
                            current_time = time.time()
                            if current_time >= end_time:
                                leds.off()
                                jasonCatInformation = {
                                    'idCat': id_cats,
                                    'nameCat': names,
                                    'foodGive': number,
                                    'idTank': id_tank
                                }
                                break
                            elif number >= food_give * 0.97:
                                device.value = 0
                                data = ser.readline().decode('utf-8').rstrip()
                                number = convert_to_float(data) 
                                current_time = time.time()
                                breakLoad = current_time + 2 
                                print("motor stop")
                                while True:
                                    current_time = time.time()
                                    print(number)
                                    if current_time >= breakLoad:
                                        leds.off()
                                        jasonCatInformation = {
                                            'idCat': id_cats,
                                            'nameCat': names,
                                            'foodGive': number,
                                            'idTank': id_tank
                                        }
                                        break
                                break
                            elif  food_give < 20:
                                device.value = 0.38
                            elif number > food_give * 0.85:
                                device.value = 0.4
                                print("food is > 80%")
                            elif number > food_give * 0.65:
                                device.value = 0.6
                                print("food > 65%")
                            elif number > 0:
                                device.value = 0.7

                        else:
                            print("wait")
                            current_time = time.time()
                            if current_time >= end_time:
                                break

            except KeyboardInterrupt:
                print("Program interrupted.")
            finally:
                motor1.close()
                motor2.close()
                if ser and ser.is_open:
                    print("ser close")
                    #ser.close()
                return jasonCatInformation
    except Exception as e:
        print(f"An error occurred: {e}")


def loadFoodEnd(jasonCatInformation):   
    try:
        found_comport()
        if ser_obj:
            ser = ser_obj
            id_cats = jasonCatInformation["idCat"]
            food_give = jasonCatInformation["foodGive"]
            current_time = time.time()
            play_loop_time = current_time + 5
            try:
                while True:
                    if ser.in_waiting:
                        # Read and decode data from the serial port
                        data = ser.readline().decode('utf-8').rstrip()                 
                        number = convert_to_float(data)
                        if number is not None:
                            Food_remaining = number  # Use the float value directly
                            print(Food_remaining)
                            current_time = time.time()
                            if current_time >= play_loop_time:
                                Food_eat = food_give - Food_remaining
                                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                break
                        else:
                            play_loop_time = current_time + 5
                    time.sleep(0.1)  # Sleep to avoid high CPU usage

            except KeyboardInterrupt:
                print("Program interrupted.")
    except Exception as e:
        print("Error occurred while reading from serial port:", e)

    try:
        # URL สำหรับเซิร์ฟเวอร์
        url = 'http://localhost:3000/setEatinformation'

        # สร้างข้อมูลในรูปแบบ JSON
        data = {
            'ID_Cat': id_cats,
            'food_give': food_give,
            'Food_eat': Food_eat,
            'Food_remaining': Food_remaining,
            'CurrentTime': timestamp
        }
        print(data)
        # ส่งคำขอ POST
        try:
            response = requests.post(url, json=data)  # ใช้ POST แทน GET
            response.raise_for_status()  # ตรวจสอบสถานะการตอบกลับ
            print('Update successful:', response.json())  # แสดงผลลัพธ์
        except requests.RequestException as e:
            print('Error:', e)  # แสดงข้อผิดพลาดถ้ามี
                    
    except requests.RequestException as e:
        print('Error occurred while processing responseCat:', e)
    except serial.SerialException as e:
        print('Serial port error:', e)
    finally:
        if ser and ser.is_open:
            ser.close()
        print("Serial connection closed.")

        
    

jasonCatInformation = {
    'idCat': 1,
    'nameCat': "names",
    'foodGive': 60,
    'idTank': 2
}
a = loadCell(jasonCatInformation)
print(a)
time.sleep(10)
loadFoodEnd(a)
#print(c)
