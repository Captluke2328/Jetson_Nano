#!/usr/bin/python3

import cv2
import jetson.utils
import jetson.inference
import numpy as np
model = jetson.inference.detectNet("SSD-Mobilenet-v2")
width = 640
height = 320

cam= cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink')

camx= cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink')

#cam = cv2.VideoCapture('/dev/video0')
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, width )
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height )

# Opening the camera
while cam.isOpened():

    ret, frame = cam.read()
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    
    #Convert numpy ndarray into CUDA memory to pass to the detector
    img = jetson.utils.cudaFromNumpy(frame_rgba)
    
    detections = model.Detect(img, width, height, "box,labels,conf")
    
    #Convert CUDA memory to numpy
    conv1 = jetson.utils.cudaToNumpy(img, width, height, 4)        
    conv2 = cv2.cvtColor(conv1, cv2.COLOR_RGBA2RGB).astype(np.uint8)
    conv3 = cv2.cvtColor(conv2, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", conv3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        SystemExit(0)

cam.release()
cv2.destroyAllWindows()
