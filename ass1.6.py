#!/usr/bin/env python

import cv2
import time

cap = cv2.VideoCapture(1)
pTime = 0
while True:

    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = gray.shape
    max = 0
    for i in range(rows):
        for j in range(rows):
            if gray[i][j] > max:
                max = gray[i][j]
                x = i
                y = j
     #FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (5, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    cv2.circle(img, (x, y), 10, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
