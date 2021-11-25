import cv2
import numpy as np
import time

# load the COCO class names
classNames = []
with open('object_detection_classes_coco.txt', 'r') as f:
   classNames = f.read().split('\n')
 
# get a different color array for each of the classes
COLORS = np.random.uniform(0, 255, size=(len(classNames), 3))

print(classNames)

modelCongiguration = 'yolov3_320.cfg'
modelWeights = 'yolov3_320.weights'
net = cv2.dnn.readNetFromDarknet(modelCongiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
cap = cv2.VideoCapture(0)
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w = int(det[2]*wT)
                h = int(det[3]*hT) 
                x = int(det[0]*wT)-w/2
                y = int(det[1]*hT)-h/2
                x = int(x)
                y = int(y)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
   
    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold, nmsThreshold)
    #print(indices)
    for i in indices:
        i = i
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        print(x,y,w,h)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 2)
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)







while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], 1, crop=False)
    start = time.time()
    net.setInput(blob)

    layerNames = net.getLayerNames()
    #print(layerNames)
    outputNames = []
    outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames)

    outputs = net.forward(outputNames)
    end = time.time()
    # print(type(outputs))
    # print((outputs[1].shape))
    # print((outputs[2].shape))
    # print(type(outputs[0][0]))
    fps = 1 / (end-start)
    findObjects(outputs, img) 
    cv2.putText(img, f"{fps:.2f} FPS", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(1)