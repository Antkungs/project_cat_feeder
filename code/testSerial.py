import time
import serial
import serial.tools.list_ports

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
    # รอให้ Serial Port เริ่มต้น
    time.sleep(1)
found_comport()
while True:
    ser = ser_obj
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        print(data)
        time.sleep(0.5)