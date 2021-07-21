#! /usr/bin/env python3

import cv2
import numpy as np
import time
import math
import os

from Modules import Hand_tracking_module as hTrack

###########################################
import mediapipe as mp
#  Check the link to get which point refer to which part of hand
#  https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model 
###########################################
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam) # camera setting
cap.set(4, hCam)
###########################################

detector = hTrack.handDetector(detectionConfi=0.75)

###########################################
###### Image loading and resizing #######
folderPath = "Finger"
myList = os.listdir(folderPath)
myList.sort()
overlayList = []
for imgpath in myList:
    image = cv2.imread(f'{folderPath}/{imgpath}')
    overlayList.append(cv2.resize(image, (200, 250)))
print(len(overlayList))
###########################################

pTime, cTime = 0, 0
tipIds = [4, 8, 12, 16, 20] # finger tips landmark id

while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []
        # for thumb (different scenario)
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # for the rest 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)

        if totalFingers != 0:
            h, w, c = overlayList[totalFingers-1].shape
            img[0:h, 0:w] = overlayList[totalFingers-1]
        
            cv2.rectangle(img, (20, 300), (170,450), (0,255,0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 430), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (500, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)