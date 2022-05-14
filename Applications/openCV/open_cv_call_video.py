import cv2
import numpy as np

cap = cv2.VideoCapture("Resources/robot.mp4")
while True:
    success, img = cap.read()
    cv2.imshow("robot", img)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

