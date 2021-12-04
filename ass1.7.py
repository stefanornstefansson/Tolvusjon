#!/usr/bin/env python

import cv2
import time
import numpy as np

#rtsp://admin:123456@192.168.0.333
#rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_175k.mov
#http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
#wCam, hCam = 640, 480
cap = cv2.VideoCapture('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')
#cap.set(3, wCam)
#cap.set(4, hCam)
pTime = 0

while True:
    success, img = cap.read()

    #FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (5, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    #Brightest spot
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(img, maxLoc, 10, (255, 0, 0), 2)

    #Reddest spot
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lb = np.array([-5, 0, 100])
    ub = np.array([5, 255, 255])
    mask = cv2.inRange(img_hsv, lb, ub)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_hsv[:,:,1], mask)
    cv2.circle(img, maxLoc, 10, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
