#!/usr/bin/env python

import cv2
import time
import numpy as np
from numpy import linalg as LA

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]

cap = cv2.VideoCapture(0)
pTime = 0
temp = np.ndarray
delta = 5

while True:
    success, img = cap.read()
    img = img[0:640, 0:480]
    canny = cv2.Canny(img, 0, 400)
    #croped = cv2.bitwise_and(img[:, :, 0], canny)
    #print(croped.shape)
    
    temp = np.argwhere(canny > 0)
    
    if len(temp) != 0:
        #print('before: ', len(temp))
        points = temp.shape[0]
        a = np.array
        b = np.array
    for n in range(4):
        for k in range(30):
            rand1 = np.random.randint(0,len(temp))
            rand2 = np.random.randint(0,len(temp))
            p1 = temp[rand1]
            p2 = temp[rand2]
            inliers = 2
            number = inliers
            temp = temp[0:len(temp):][:]
           # print('after: ', len(temp))
            for i in range(temp.shape[0]):
                d = LA.norm(np.cross(p2-p1, p1-temp[i]))/LA.norm(p2-p1)
                a = np.append(a, temp[i])
                if d < delta:
                    inliers += 1
            if inliers >= number:
                number = inliers
                point1 = p1
                point2 = p2
       # b = np.delete(temp, a)
        
            
    else:
        points = 100
        point1, point2 = [0, 0], [0, 0]
        inliers = 2
        number = inliers
    print(number)

    
    
    if number > 200:
        cv2.line(img, [point1[1], point1[0]], [point2[1], point2[0]], (255, 255, 255), thickness=10, lineType=8)
        cv2.circle(img, [point1[1], point1[0]], 10, (255, 0, 0), 2)
        cv2.circle(img, [point2[1], point2[0]], 10, (255, 0, 0), 2)
        
        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (480, 640), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
