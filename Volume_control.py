import cv2
import numpy as np
import time
import math

# created module using MediaPipe
from Modules import Hand_tracking_module as hTrack

###########################################
import alsaaudio as audio
# To control volume with python script we can use
#     pycaw         in window (https://github.com/AndreMiras/pycaw)
#     alsaaudio     in ubuntu (https://pypi.org/project/pyalsaaudio/)
###########################################
#  Check the link to get which point refer to which part of hand
#  https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model 
###########################################
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam) # camera setting
cap.set(4, hCam)
###########################################

detector = hTrack.handDetector(detectionConfi=0.75)
volume = audio.Mixer()

pTime = 0
minVol, maxVol = 0, 100
vol_set = 0
vol_get = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList) # get position of all points on a hand
    if len(lmList) != 0:
        # for this project we use Thumb_Tip and Index_finger_tip
        # print(lmList[4], lmList[8]) 
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2 # floor devision
        cv2.circle(img, (x1,y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(img, (cx,cy), 5, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        vol_set = np.interp(length, [25, 250], [minVol, maxVol])
        volume.setvolume(int(vol_set))

        if length <= 25:
            cv2.circle(img, (cx,cy), 10, (0, 0, 255), cv2.FILLED)

    vol_get = np.interp(volume.getvolume()[0], [0,100],[400, 150])
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, 400), (85, int(vol_get)), (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f"Vol: {volume.getvolume()[0]}%", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)