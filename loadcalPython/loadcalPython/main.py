import socket
import time
from datetime import datetime, timedelta

import requests


ports = 3000
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
    ip = get_ip_address()
    url = f"http://{ip}:{ports}"
    
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
    
    # Write HTML content to a file
    with open('ip_address.html', 'w') as file:
        file.write(html_content)
    
    # Return the HTML content as the response
    return html_content

def check_internet(url='https://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        # Return True if the status code is 200 (OK)
        return response.status_code == 200
    except requests.ConnectionError:
        # Return False if there is a connection error
        return False
    
def cantConnect(signal):
    with open('signal.txt', 'w') as file:
        file.write(signal)
        
def main():
    if not check_internet() : #(noInternet):
        checkTime = datetime.now() + timedelta(seconds=1)
        count = 0
            #ปิดไวไฟ Hot Sport
            #time.sleep(0.5)
            #เปิดไวไฟเพื่อทำการเชื่อมต่อ
            #time.sleep(0.5)
        while True:
            #สั่งเชื่อมไวไฟ โดยอ่านค่าจาก .txt
            current_time = datetime.now()
            current_time_string = current_time.strftime("%H:%M:%S")
            if check_internet():
                print("Connect internet")
                createIndexCanConnect()
                break
            if current_time >= checkTime: #if ใช้เวลาเชื่อมต่อนาน => timeout 
                #สั่งเชื่อมไวไฟ โดยอ่านค่าจาก .txt
                checkTime = current_time + timedelta(seconds=1)
                count+=1
                print(current_time_string)
                print(count)
            if count == 10:
                print("Cant Connect Internet")
                cantConnect("0")
                #ปิดไวไฟ
                #time.sleep(0.5)
                #เปิดไวไฟ Hot Sport
                break
                
            time.sleep(0.1)
    else: #(haveInternet):
        print("haveInternet")
        createIndexCanConnect()
        

main()