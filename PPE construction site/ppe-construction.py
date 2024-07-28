from ultralytics import YOLO
import cv2
import cvzone
import math

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('../video/ppt-2.mp4')

# cap.set(3, 640)
# cap.set(4, 480)
model = YOLO("best.pt")
clasNames = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
             'Person', 'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery',
             'mini-van', 'sedan', 'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']
mycolour = (0, 0, 255)
while True:
    success, img = cap.read()
    result = model(img, stream=True)
    for r in result:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            conf = math.ceil((box.conf[0] * 100)) / 100
            # print("value", conf)
            cls = int(box.cls[0])
            currentClass = clasNames[cls]
            if conf > 0.5:
                if currentClass == "Hardhat" or currentClass == "Safety Vest" or currentClass == "Mask":
                    mycolour = (0, 255, 0)
                elif currentClass == "NO-Hardhat" or currentClass == "NO-Safety Vest" or currentClass == "NO-Mask":
                    mycolour = (0, 0, 255)
                else:
                    mycolour = (255, 0, 0 )
                cvzone.putTextRect(img, f'{clasNames[cls]} {conf}', (max(0, x1), max(35, y1-20)), scale=0.5, thickness=1,
                                   colorB=mycolour, colorT=(255, 255, 255), colorR=mycolour, offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), mycolour, 3)

    cv2.imshow("image", img)
    cv2.waitKey(2)
