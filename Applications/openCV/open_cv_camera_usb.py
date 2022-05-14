import cv2

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('/dev/video0')

while True:
    success, img = cap.read()
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
    