from datetime import datetime, timedelta
import os
import socket
import subprocess
import time
import requests
import connectNetwork as cnt
from gpiozero import OutputDevice
current_time = datetime.now()
checkTime = datetime.now() + timedelta(seconds=10)
ports = 3000
led = OutputDevice(16)
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to an external server to get the local IP address
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error: {e}"
    
def createIndexCanConnect():

    directory = r'/var/www/html/txt/'
    file_name = 'ip_address.html'
    ip = get_ip_address()
    url = f"http://{ip}:{ports}"
    file_path = os.path.join(directory, file_name)
    # Define the HTML template
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IP Address</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }}
            h1 {{
                color: #4CAF50;
                text-align: center;
                margin-top: 50px;
            }}
            p {{
                text-align: center;
                font-size: 18px;
            }}
            a {{
                color: #1E90FF;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style=" color: #4CAF50;">Your Web Application</h1>
            <p><a href="{url}" target="_blank">Click Here</a></p>
        </div>
    </body>
    </html>
    '''

    with open(file_path, 'w') as file:
        file.write(html_content)
    
    return html_content

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to an external server to get the local IP address
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error: {e}"
    
def get_current_ssid_windows():
    try:
        # Run the command to get the current Wi-Fi connection details
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Find the line with the SSID
            lines = result.stdout.split('\n')
            for line in lines:
                if 'SSID' in line:
                    ssid = line.split(':')[1].strip()
                    return ssid
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_current_ssid_linux():
    try:
        # Run the iwgetid command to get the SSID of the connected network
        result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True, check=True)
        
        # The result stdout contains the SSID
        ssid = result.stdout.strip()
        return ssid
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    
def showIPandSSID():
    ip = get_ip_address()
    ssid = get_current_ssid_windows()
    print(f"{ssid}\n{ip}:3000")

def write_to_txt(content):
    try:
        file_path = r'/var/www/html/txt/signal.txt'
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file: {e}")

def writePage(content):
    try:
        file_path = r'/var/www/html/txt/signalPage.txt'
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file: {e}")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found.")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None
    
def check_internet(url='https://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        # Return True if the status code is 200 (OK)
        return response.status_code == 200
    except requests.ConnectionError:
        # Return False if there is a connection error
        return False

def closeWifi():
    command = f"sudo nmcli device disconnect wlan0 "
    # Execute the command
    subprocess.run(command, shell=True)
    
def openHotspot():
    command = f'sudo nmcli connection up Hotspot'
    subprocess.run(command, shell=True)
    
def closeHotsport():
    command = f'sudo nmcli connection down Hotspot'
    subprocess.run(command,shell=True)
    
def mainRun():
    global hotspot
    current_time = datetime.now()
    checkTime = datetime.now() + timedelta(seconds=1)
    closeHotsport()
    if not check_internet(): #(noInternet):
        print("no internet")
        time.sleep(0.5)
        cnt.main()         
        if not check_internet():
            writePage("cant")
            write_to_txt("0")
            print(f"Cant Connect internet" )
            hotspot = True
     

def runThread():
    import subprocess
    script_path = r"/home/antkung/Desktop/projects/code/runThread.py"

    try:
        result = subprocess.run(["python3", script_path], capture_output=True, text=True, check=True)
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        
hotspot = True
while True:
    file_path = r'/var/www/html/txt/signal.txt'
    content = read_file(file_path)
    current_time = datetime.now()
    print(content)
    if content:
        led.on()
        if check_internet():
            led.off()
            createIndexCanConnect()
            writePage("can")
            print(f"Connect internet {get_ip_address()}" )
            print("runThread")
            runThread()
        if not check_internet() and hotspot:
            led.on()
            hotspot = False
            openHotspot()
        if content == "1":
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
            led.on()
            time.sleep(0.5)
            led.off()
            mainRun()
    else:
        print("no data")
    time.sleep(10)
