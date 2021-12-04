#!/usr/bin/env python

import cv2

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    print(maxLoc)
    cv2.circle(img, maxLoc, 10, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
