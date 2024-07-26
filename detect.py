import time
import cv2
import Time
import LineNotifi as line
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

def detect():
    global frame2 , current_time
    model = YOLO("model/countCat.pt")
    model2 = YOLO("model/classification.pt") #model หาแมว
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result1 = model(frame)
        result2 = model2(frame) 
        try:  
            #ตีกรอบแมวธรรมดา
            for r in result1:
                annotator = Annotator(frame)    
                boxes = r.boxes
                for box in boxes:        
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)]) 
            frame = annotator.result() 

            current_time = time.time()

            if(result1[0].boxes.cls.tolist().count(0) > 1): #เช็คแมวว่ามี > 1 ตัว
                print("เจอแมวมากกว่า 1 ตัว")
                updated_time = current_time + 5
                
            elif(result1[0].boxes.cls.tolist().count(0) == 1 and current_time >= updated_time): #เช็คแมวว่ามี 1 ตัว
                for result in result2:
                    probs = result.probs  # Probs object for classification outputs
                    if(probs.top1conf > 0.5): #id classification
                        filename = "temp.jpg"  #ถ่ายภาพเพื่อเก็บสถานะไว้ส่งไปยังไลน์
                        cv2.imwrite(filename, frame)
                        #line.send_image("temp.jpg", model2.names[probs.top1])
                        #select = probs.top1 + 1
                        #ime.getTime(select) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา
                        while True:   
                            print(probs.top1+1)
                            print(model2.names[probs.top1])
                            ret, frame = cap.read()
                            if not ret:
                                break
                            result1 = model(frame)
                            current_time = time.time() 
                            if(result1[0].boxes.cls.tolist().count(0) >= 1):
                                play_loop_time = current_time + 5
                            elif(current_time > play_loop_time):
                                break


                    else:
                        print("NOT SURE")
                
                #Time.getTime(name.loc[0, 'class']) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา

                #print(name.loc[0, 'class']) #บอกว่าแมว class ไหน
                    #if found == False and count == 0:
                       # count = 1
                        #found = True
                    #if count == 1:
                       # updated_time = current_time + timedelta(seconds=5)
                        #count = 0
                       # print(count)
                    #หน่วง 5 วิเพื่อทำการยืนยัน
                    #if current_time >= updated_time:
                        #found == False
                        #count = 0
                        #filename = "temp.jpg"  #ถ่ายภาพเพื่อเก็บสถานะไว้ส่งไปยังไลน์
                        #cv2.imwrite(filename, frame)
                        #print("getTime")
                        #line.send_image("j5Vy1V07apBG2tuWIuJ4S5aolnhM7VhBRla7ZdDnYgh", "temp.jpg", "message")
                        #Time.getTime(name.loc[0, 'class']) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา

            else:
                print("do noting")

        except Exception as e:
            #updated_time = current_time + 5
            print("ERROR")

        current_time = time.time()
        updated_time = current_time + 5
        frame2 = frame

        cv2.imshow("result",frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect()

