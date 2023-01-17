import cv2
from datetime import datetime

print("Package imported")

cap = cv2.VideoCapture(0)
w = int(cap.get(3))
h = int(cap.get(4))

print(w,h)

path = "D:\\For_Referene\\Machine_Learning_Sample_Project_Tutorial\\Python Project\\Open_CV_Project\\record\\"
curr_timestamp = int(datetime.timestamp(datetime.now()))

writer= cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30 ,(w,h))

while True:
    success, img = cap.read()
    
    
    writer.write(img)
            
    cv2.imshow("Capture",img)
            
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

cap.release()
writer.release()

cv2.destroyAllWindows()
