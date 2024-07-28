from ultralytics import YOLO
import cv2
import cvzone
import math
import pokerHandFunction

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('../video/bikes2.mp4')

cap.set(3, 640)
cap.set(4, 480)
model = YOLO("../yolo-weights/yolov8l.pt")
clasNames = ['0', '1', '10', '10C', '10D', '10H', '10S', '11', '12', '13', '14', '16', '17', '18', '19', '2', '21',
             '22', '23', '24', '25', '26', '27', '28', '29', '2C', '2D', '2H', '2S', '3', '30', '31', '32', '33', '34',
             '35', '37', '38', '39', '3C', '3D', '3H', '3S', '4', '40', '41', '42', '43', '44', '46', '47', '48', '49',
             '4C', '4D', '4H', '4S', '5', '50', '51', '52', '53', '55', '5C', '5D', '5H', '5S', '6', '6C', '6D', '6H',
             '6S', '7', '7C', '7D', '7H', '7S', '8', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH',
             'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']

while True:
    success, img = cap.read()
    result = model(img, stream=True)
    hand = []
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
            cvzone.putTextRect(img, f'{clasNames[cls]} {conf}', (max(0, x1), max(35, y1-20)), scale=1, thickness=1)
            if conf > 0.5:
                hand.append(clasNames[cls])
    print(hand)
    hand = list(set(hand))

    if len(hand) == 5:
        result = pokerHandFunction.findPokerHand(hand)
        cvzone.putTextRect(img, f'Your Hand : {result}', (300, 750), scale=3, thickness=5)
        print(result)
    cv2.imshow("image", img)
    cv2.waitKey(2)
