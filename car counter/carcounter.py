from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

cap = cv2.VideoCapture('../video/cars2.mp4')

model = YOLO("../yolo-weights/yolov8l.pt")
clasNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
             "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
             "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
             "handbag" "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
             "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
             "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli"
             "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
             "dining table", "toilet", "monitor", "Laptop", "mouse", "remote", "keyboard", "cell phone",
             "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
             "teddy bear", "hair drier", "toothbrush"]
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
limits = [700, 200, 200, 100]
totalCount = 0
while True:
    success, img = cap.read()
    detections = np.empty((0, 5))
    result = model(img, stream=True)
    for r in result:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 3)
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            # print("value", conf)
            cls = int(box.cls[0])
            currentclass = clasNames[cls]
            if currentclass == 'car' and conf > 0.3:
                # cvzone.putTextRect(img, f'{currentclass} {conf}', (max(0, x1), max(35, y1-20)), scale=0.6,
                # thickness=1, offset=3)
                # cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                curretArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, curretArray))
    resultsTracker = tracker.update(detections)

    for results in resultsTracker:
        x1, y1, x2, y2, id = results
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 0))
        cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(35, y1 - 20)), scale=2, thickness=3,
                           offset=10)
        cx, cy = x1+w//2, y1+h//2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        if limits[0] > cx > limits[2] and limits[1] - 15> cy > limits[3]+15:
            totalCount+=1

    cvzone.putTextRect(img, f'count :{totalCount}', (50, 50))

    resultsTracker = tracker.update(detections)
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
    cv2.imshow("image", img)

    cv2.waitKey(1)
