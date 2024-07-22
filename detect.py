import time
import cv2
import torch
#import Time
import LineNotifi as line
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

def main():
    cap = cv2.VideoCapture(0)
    count = 0
    model = YOLO("model/best.pt") #model หาแมว
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = model(frame)
        print(result[0].cls.tolist())
        try:      
            #for r in result:
        
             #   annotator = Annotator(frame)
                
              #  boxes = r.boxes
               # for box in boxes:
                    
                #    b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                  #  c = box.cls
                 #   annotator.box_label(b, model.names[int(c)])
                
            #rame = annotator.result() 
            if(result[0].boxes.cls.tolist().count(0) > 1): #เช็คแมวว่ามี > 1 ตัว
                print("เจอแมวมากกว่า 1 ตัว")
                count = 0
                
            elif(result[0].boxes.cls.tolist().count(0) == 1): #เช็คแมวว่ามี 1 ตัว
                #print(name.loc[0, 'class']) #บอกว่าแมว class ไหน
                if(result[0].boxes.cls.tolist().count(0) == 1):
                    #time.sleep(1)
                    #count += 1
                    print(count)
                    #หน่วง 5 วิเพื่อทำการยืนยัน
                    #if(count == 5):
                        #filename = "temp.jpg"  #ถ่ายภาพเพื่อเก็บสถานะไว้ส่งไปยังไลน์
                        #cv2.imwrite(filename, frame)
                        #count = 0
                        #print("getTime")

                        #line.send_image("j5Vy1V07apBG2tuWIuJ4S5aolnhM7VhBRla7ZdDnYgh", "temp.jpg", "message")
                        
                        #Time.getTime(name.loc[0, 'class']) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา

            else:
                count = 0
                print("do noting")

        except Exception as e:
            print("NON FOUND")

        cv2.imshow("result",frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    
    cap.release()
    cv2.destroyAllWindows()


main()

