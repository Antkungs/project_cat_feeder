import cv2
import torch
from ultralytics import YOLO

def main():
    modelCheck = torch.hub.load('ultralytics/yolov5', 'custom', "model/cat3.pt")
    cap = cv2.VideoCapture(0)  # Specify the path to your video file here

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result2 = modelCheck(frame)
        print(result2.pandas().xyxy[0])
        try:      
            result2.pandas().xyxy[0]
            print("Object Found")
        except Exception as e:
            print("Object Not Found")
        cv2.imshow("result", frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()