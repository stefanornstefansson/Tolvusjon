#!/usr/bin/env python

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while True:

    success, img = cap.read()

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lb = np.array([-5, 0, 100])
    ub = np.array([5, 255, 255])

    mask = cv2.inRange(img_hsv, lb, ub)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_hsv[:,:,1], mask)
    
    cv2.circle(img, maxLoc, 10, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
