import serial
import time
from datetime import datetime
import requests

# ใช้พอร์ต Serial ที่ Raspberry Pi
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# รอให้ Serial Port เริ่มต้น
time.sleep(2)
def convert_to_float(data_str):
    try:
        if data_str is None or data_str == '':
            return 0.0
        # Convert the string to a float
        return float(data_str)
    except ValueError:
        # Handle the case where conversion fails
        print(f"Error converting '{data_str}' to float.")
        return None

def loadCell(food_give,id_tank):
    try:
        motor1 = OutputDevice(23)
        motor2 = OutputDevice(24)
        led1 = OutputDevice(2)
        led1.off()
        led2 = OutputDevice(3)
        led2.off()
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
        food_give = convert_to_float(food_give)
        while True:
            if ser.in_waiting > 0:
                # Read and decode data from the serial port
                data = ser.readline().decode('utf-8').rstrip()
                number = convert_to_float(data)
                print(number)
                leds.on()
                device.value = 1
                print("motor run")
                if number is not None:
                    if number >= food_give:
                        leds.off()
                        device.value = 0
                        print("motor stop")
                        sleep(3) 
                        break

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        ser.close()
        led1.close()
        led2.close()
        motor1.close()
        motor2.close()
        print("Serial connection closed.")

def loadFoodEnd(select):
    ser = None  # Initialize ser variable
    
    try:
        # Initialize the serial port
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Adjust port and baud rate as needed

        response_cat = requests.get('http://localhost:3000/catinformation')
        response_cat.raise_for_status()  # Will raise HTTPError for bad responses
        cats = response_cat.json()  # Get all data from the API
        
        for cat in cats:
            if cat['id_cat'] == select:
                id_cat = cat['id_cat']
                food_give = cat['food_give']  # Amount of food to give (grams)
                current_time = time.time()
                play_loop_time = current_time + 5

                try:
                    while True:
                        if ser.in_waiting > 0:
                            data = ser.readline().decode('utf-8').rstrip()
                            number = convert_to_float(data)
                            if number is not None:
                                Food_eat = number  # Use the float value directly
                                print(Food_eat)
                                current_time = time.time()
                                if current_time >= play_loop_time:
                                    break
                            else:
                                play_loop_time = current_time + 5
                        time.sleep(0.1)  # Sleep to avoid high CPU usage

                except KeyboardInterrupt:
                    print("Program interrupted.")
                except Exception as e:
                    print("Error occurred while reading from serial port:", e)
                
                # Make sure Food_eat is defined
                if 'Food_eat' in locals():
                    Food_eat = int(Food_eat)
                    Food_remaining = food_give - Food_eat
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    url = (f'http://localhost:3000/setEatinformation?ID_Cat={id_cat}&food_give={food_give}&Food_eat={Food_eat}&Food_remaining={Food_remaining}&CurrentTime={timestamp}')
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        print('Update successful:', response.json())
                    except requests.RequestException as e:
                        print('Error:', e)
                else:
                    print("No valid food amount read from serial.")
                    
    except requests.RequestException as e:
        print('Error occurred while processing responseCat:', e)
    except serial.SerialException as e:
        print('Serial port error:', e)
    finally:
        if ser and ser.is_open:
            ser.close()
        print("Serial connection closed.")


