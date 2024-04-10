import time
import requests
import cv2
import tets

url = 'https://notify-api.line.me/api/notify'

def send_text(token, text):
    LINE_HEADERS = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    session_post = requests.post(url, headers=LINE_HEADERS , data = {'message':text})
    print(session_post.text)

def send_image(token, image_path, message):
    file_img = {'imageFile': open(image_path, 'rb')}
    LINE_HEADERS = {'Authorization':'Bearer '+token}
    session_post = requests.post(url, headers=LINE_HEADERS, files=file_img, data={'message': message})
    print(session_post.text)

def sendCatEat(token, name):
    image_path = '01.jpg'
    message = "แจ้งเตือนการกินอาหาร :\n{} มากินอาหาร".format(name)
    send_image(token, image_path, message)

def sendTankLow(token,id):
    message = "แจ้งเตือนอาหารเม็ดในถังเก็บ :\nถังที่ {} อาหารใกล้จะหมดกรุณาเติมอาหารเม็ด".format(id)
    send_text(token,message)

def sendTankFull(token):
    message = "แจ้งเตือนอาหารเม็ดในถังเหลือ :\nอาหารเม็ดใกล้จะเต็มแล้วกรุณานำไปกำจัด"
    send_text(token,message)

if __name__ == "__main__":
    token = 'mUPbblGzEZ3vSddDNOaBBiqHezJ0NBj3aRkT8XSFlbU'
    sendCatEat(token, tets.name)
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

