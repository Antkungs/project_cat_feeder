
import socket
import subprocess
import time
import LineNotifi as line
import urllib.request
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to an external server to get the local IP address
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error: {e}"
    
def read_credentials_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            token = lines[2].strip()
            return token
    except FileNotFoundError:
        print("File not found.")
        return None, None
    

def check_internet():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=2)
        return True
    except urllib.request.URLError:
        return False
    
def connect_to_wifi(ssid, password):
    command = f"sudo nmcli device wifi connect '{ssid}' password '{password}'"
    subprocess.run(command, shell=True)
    
def closeHotspot():
    command = 'sudo nmcli connection down Hotspot'
    subprocess.run(command, shell=True)

while True:
    if check_internet():
        file_path = '/var/www/html/txt/wificonfig_.txt'
        token = read_credentials_from_file(file_path)
        ip = get_ip_address()
        url = f"\nWeb Application\nhttp://{ip}:{3000}"
        try:
            line.send_text_check(token,url)
        except Exception as e:
            print(f"Error: {e}")
        break
    closeHotspot()
    time.sleep(5)
    connect_to_wifi("Aaa","aaaaaaaa")
    time.sleep(15)
    print("2")