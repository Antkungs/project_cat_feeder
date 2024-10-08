import serial
import serial.tools.list_ports
import time
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

def convert_to_float(data_str):
    try:
        if data_str is None or data_str.strip() == '':
            return 0.0
        return float(data_str)
    except ValueError:
        print(f"Error converting '{data_str}' to float.")
        return None

def main():
    found_comport()
    current_time = time.time()
    end_time = current_time + 60
    if ser_obj:
        try:
            while True:
                if ser_obj.in_waiting > 0:
                    # Read and decode data from the serial port
                    data = ser_obj.readline().decode('utf-8').rstrip()                 
                    number = convert_to_float(data)
                    print(current_time)
                    if number is not None:
                        print(f"{number}")
                        current_time = time.time()
                    if current_time >= end_time:
                        break
                    
                # Sleep briefly to avoid overwhelming the CPU
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            if ser_obj:
                ser_obj.close()
                print(f"Serial port {ser_obj.portstr} closed")

if __name__ == "__main__":
    main()
