import requests

url = 'https://notify-api.line.me/api/notify'

def getToken():
    try:
        responseToken = requests.get('http://localhost:3000/notification')
        
        if responseToken.status_code == 200:
            datas = responseToken.json()
            # Assuming datas is a list of dictionaries with 'token' key
            for data in datas:
                token = data['token']
            print(token)
            return token
        else:
            print('Error:', responseToken.text)
    except requests.exceptions.RequestException as e:
        print('Error occurred while making request:', e)
    except Exception as e:
        print('Error occurred while processing responseToken:', e)
    
def send_text(text):
    token = getToken()
    LINE_HEADERS = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    session_post = requests.post(url, headers=LINE_HEADERS , data = {'message':text})
    print(session_post.text)

def send_image( image_path, message):
    token = getToken()
    file_img = {'imageFile': open(image_path, 'rb')}
    LINE_HEADERS = {'Authorization':'Bearer '+token}
    session_post = requests.post(url, headers=LINE_HEADERS, files=file_img, data={'message': message})
    print(session_post.text)

def sendCatEat(name , current_time):
    image_path = 'temp.jpg'
    message = "\nแจ้งเตือนการกินอาหาร :\n{} มากินอาหาร เวลา : {} น.".format(name,current_time)
    send_image(image_path, message)

def sendTankLow(id):
    try:
        url = f'http://localhost:3000/getNameTank/{id}'
        responseTank = requests.get(url)
        
        if responseTank.status_code == 200:
            datas = responseTank.json()
            if datas:  # Assuming the response is a list and can have multiple items
                for data in datas:
                    name_tank = data.get('name_tank')
                    
                message = "\nแจ้งเตือนอาหารเม็ดในถังเก็บ :\nอาหารถัง {} ใกล้จะหมดกรุณาเติมอาหารเม็ด".format(name_tank)
                send_text(message)
            else:
                print('Error: Empty response data')
        else:
            print(f'Error: Status Code {responseTank.status_code}, {responseTank.text}')
    
    except requests.exceptions.RequestException as e:
        print('Error occurred while making request:', e)

    except Exception as e:
        print('Error occurred:', e)

def sendTankFull():
    message = "\nแจ้งเตือนอาหารเม็ดในถังเหลือ :\nอาหารเม็ดใกล้จะเต็มแล้วกรุณานำไปกำจัด"
    send_text(message)

def start():
    message = "\nเริ่มการทำงาน"
    send_text(message)

"""
    while True:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        
        cv2.imshow("Captured Image", frame)
        
        key = cv2.waitKey(1)
        if key == ord('c'):  # ถ้าผู้ใช้กด 'c'
            filename = "01.jpg"
            cv2.imwrite(filename, frame)
            sendCatEat(token, 'ส้ม')
        elif key == 27:  # ถ้าผู้ใช้กด ESC
            break
    cap.release()
    cv2.destroyAllWindows()
""" 
