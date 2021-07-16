#! /usr/bin/env python3

import cv2
import mediapipe as mp
import time

# will create class
class handDetector(): # class
    def __init__(self, mode=False, maxHands=2, detectionConfi=0.5, trackConfi=0.5): # for mpHands.Hands()
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfi = detectionConfi
        self.trackConfi = trackConfi

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 
                                        self.detectionConfi, self.trackConfi) # use only RGB image
        self.mpDraw = mp.solutions.drawing_utils

    # finding Hand-landmarks
    def findHands(self, img, draw=True): # hand finding method
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert to RGB
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: # for multiple hands
                if draw: # check draw or not
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # finding location of the hand-landmarks on webCam
    def findPosition(self, img, handNo=0, draw=True):
        # handNo = 0 define how many hands to draw (0 -> 1 hand)
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm) # location of each landmark points (ratio of pixel size)
                # print(img.shape) # getting image size
                h, w, c = img.shape
                coordinate_x, coordinate_y = int(lm.x*w), int(lm.y*h) # location of each landmark points (not hand) 
                lmList.append([id, coordinate_x, coordinate_y])
                if draw:
                    cv2.circle(img, (coordinate_x, coordinate_y), 10, (255, 0, 255), cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector() # call the object of class
    while True:
        success, img = cap.read()
        img = detector.findHands(img) # call the method
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) !=0:
            print(lmList, "\n")

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()