import socket
import threading
from time import sleep
from gpiozero import OutputDevice
import LineNotifi as line

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
    
def insertLine(token):
    import requests
    url = 'http://localhost:3000/insertLineFirstTime'
    payload = {
        'token': token
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print(f"Failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
 


try:
#    ledStart()
    file_path = '/var/www/html/txt/wificonfig_.txt'
    token = read_credentials_from_file(file_path)
    ip = get_ip_address()
    url = f"\nWeb Application\nhttp://{ip}:{3000}"
    try:
        line.send_text_check(token,url)
    except Exception as e:
        print(f"Error: {e}")
    try:
        insertLine(token)
    except Exception as e:
        print(f"Error: {e}")
    try:
        import api , hardwareSelect 
        thread1 = threading.Thread(target=api.detect)
        thread2 = threading.Thread(target=api.mainapi)
        thread3 = threading.Thread(target=hardwareSelect)
        #thread1.daemon = True
        #thread2.daemon = True


        thread1.start()
        thread2.start()
        thread3.start()
        
        thread1.join()
        thread2.join()
        thread3.join()
    except Exception as e:
        print(f"Error: {e}")
except Exception as e:
    print(f"Error: {e}")

print("Main thread exiting.")
