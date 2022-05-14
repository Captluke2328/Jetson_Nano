#!/usr/bin/python3

import cv2
import numpy as np

frameWidth = 640
frameHeight= 480
flip =  0

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464,format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+'! video/x-raw, width='+str(frameWidth)+', height='+str(frameHeight)+',format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = 'nvarguscamerasrc sensor_id=0 ! video/x-raw(memory:NVMM), width=3280, height=2464, framerate=21/1, format=NV12 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=720 ! nvvidconv ! nvegltransform ! nveglglessink'

camx= 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'

cap = cv2.VideoCapture(camx)

while True:
    success, img = cap.read()
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
