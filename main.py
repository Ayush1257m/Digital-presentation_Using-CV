import cv2
import os
from cvzone.HandTrackingModule import HandDetector

width , height = 1280, 720

folderPath = "presentation"

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#get the list of presentation image

pathImages = sorted(os.listdir(folderPath) , key=len)
# print(pathImages)

# variable
imgNum = 0
hs,ws = int(120*1), int(213*1)

detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:

    #import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNum])
    imgCurr = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers=  detector.fingersUp(hand)
        print(fingers)
    #adding webcam image on slides
    imgSmall = cv2.resize(img,(ws , hs))
    h, w,_ = imgCurr.shape
    imgCurr[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurr)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break