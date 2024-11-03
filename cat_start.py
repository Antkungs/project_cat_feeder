from datetime import datetime
import subprocess
import time
import requests
import urllib.request
from gpiozero import OutputDevice

def check_internet():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=2)
        return True
    except urllib.request.URLError:
        return False

def connect_to_wifi(ssid, password):
    command = f"sudo nmcli device wifi connect '{ssid}' password '{password}'"
    subprocess.run(command, shell=True)

def read_credentials_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            ssid = lines[0].strip()
            password = lines[1].strip()
            return ssid, password
    except FileNotFoundError:
        print("File not found.")
        return None, None

def runThread():
    try:
        led.on()
        command = f'/usr/bin/python3 /home/antkung/Desktop/project_cat_feeder/code/runThread.py'
        result = subprocess.run(command, shell=True)
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def main():
    file_path = '/var/www/html/txt/wificonfig_.txt'
    ssid, password = read_credentials_from_file(file_path)
    if ssid is not None and password is not None:
        print(f"SSID: {ssid}")
        print(f"Password: {password}")
        connect_to_wifi(ssid, password)
    else:
        print("Failed to read SSID and password from the file.")

def closeWifi():
    command = "sudo nmcli device disconnect wlan0"
    subprocess.run(command, shell=True)

def openHotspot():
    command = 'sudo nmcli connection up Hotspot'
    subprocess.run(command, shell=True)

def closeHotspot():
    command = 'sudo nmcli connection down Hotspot'
    subprocess.run(command, shell=True)

def mainRun():
    closeHotspot()
    if not check_internet():
        print("no internet")
        time.sleep(0.5)
        main()

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return None

def writePage(content):
    try:
        file_path = r'/var/www/html/txt/signal.txt'
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file: {e}")

led = OutputDevice(10)
writePage("0")
hotspot = False
#led.on()
time.sleep(0.5)
while True:
    file_path = r'/var/www/html/txt/signal.txt'
    content = read_file(file_path)
    current_time = datetime.now()
    print(f"Checked at {current_time}: {content}")

    try:
        if check_internet():
            print("Have internet")
            time.sleep(1)
            runThread()
        elif content == "1":
            led.on()
            print("Trying to connect...")
            writePage("0")
            hotspot = False
            closeHotspot()
            time.sleep(1)
            mainRun()
        else:
            print("no internet")
            if not hotspot:
                openHotspot()
                print("open hotspot")
                hotspot = True
            else:
                print("Hotspot is open")
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")

    if hotspot:
        for i in range(60):
            content = read_file(file_path)
            if content == "1":
                break
            else:
                led.on()
                time.sleep(0.5)
                led.off()
                time.sleep(0.5)
