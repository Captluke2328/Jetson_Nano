import cv2
import numpy as np

print("Package imported")

#cap = cv2.VideoCapture(0) ##---------> Webcam object with Id 0
cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert !  video/x-raw, format=(string)BGR ! appsink')

cap.set(3,640) ##---> Video width with Id 3
cap.set(4,480) ##---> Video height with Id 4
cap.set(10,100) ##---> Video brightness with Id 10

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        