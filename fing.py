import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np
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
gestureThreshold = 300
buttonPressed = False
buttoncntr = 0
buttonDelay = 30
detector = HandDetector(detectionCon=0.8, maxHands=1)
annotations = [[]]
annotationNumber = 0
annotationStart = False

while True:

    #import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNum])
    imgCurr = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    cv2.line(img,(0, gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers =  detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        #constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0],[width//2 , w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0,height]))
        indexFinger = xVal,yVal

        if cy <=gestureThreshold:  # if hand is at the height of the face
            annotationStart = False
            # gesture1 - left
            if fingers == [1,0,0,0,0]:
                annotationStart = False
                print("Left")
                
                if imgNum>0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNum -= 1

            # gesture2 - Right
            if fingers == [0,0,0,0,1]:
                annotationStart = False
                print("Right")
               
                if imgNum< len(pathImages)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNum += 1

        # gesture3 - show Pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurr, indexFinger,12,(0,0,255), cv2.FILLED)
            annotationStart = False

        # gesture4 - draw Pointer
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurr, indexFinger,12,(0,0,255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        # gesture 5 - eraser
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber>=0:
                    annotations.pop(-1)
                    annotationNumber -=1
                    buttonPressed = True
    else:
        annotationStart = False

    #button press iteratin
    if buttonPressed:
        buttoncntr +=1
        if buttoncntr> buttonDelay:
            buttoncntr = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if i != 0:
                cv2.line(imgCurr, annotations[i][j-1], annotations[i][j], (0,0,200),12)
    
    #adding webcam image on slides
    imgSmall = cv2.resize(img,(ws , hs))
    h, w,_ = imgCurr.shape
    imgCurr[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurr)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break