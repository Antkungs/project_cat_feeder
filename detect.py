import time
import cv2
import torch
import Time
from ultralytics import YOLO

def main():
    count = 0
    model = YOLO("model/yolov8x.pt")
    modelCheck = torch.hub.load('ultralytics/yolov5','custom',"model/cat3.pt")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result2 = modelCheck(frame)
        result = model(frame)
        try:      
            if(result[0].boxes.cls.tolist().count(15) > 1): #เช็คแมวว่ามีกี่ตัว
                print("เจอแมวมากกว่า 1 ตัว")
                count = 0
                
            elif(result[0].boxes.cls.tolist().count(15) == 1): #เช็คแมวว่ามีกี่ตัว
                name = result2.pandas().xyxy[0]
                print("give food to {}".format(name.loc[0, 'class']))
                #print(name.loc[0, 'class']) #บอกว่าแมว class ไหน
                if(result[0].boxes.cls.tolist().count(15) == 1):
                    time.sleep(1)
                    count += 1
                    #หน่วง 5 วิเพื่อทำการยืนยัน
                    if(count == 5):
                        filename = "temp.jpg"
                        cv2.imwrite(filename, frame)
                        count = 0
                        #Time.getTime(name.loc[0, 'class']) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา

            else:
                print("do noting")

        except Exception as e:
            print("NON FOUND")

        cv2.imshow("result",frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


