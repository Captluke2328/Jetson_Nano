from open_cv_color_detection import *

pid = [0.8,0.8,0]
pError = 0
w = 640
while True:
    # Step 1
    img = capture_image()
    imgContour = img.copy()
    
    # Step 2
    imgcontour, mask =  color_detection(img,imgContour)
    
    # Step 3
    contour, info = getContours(imgcontour, mask)
  
    # Step 4
    pError, speed = trackobject(info, w, pid, pError)
    
    # Step 5
    motor = moverobot(speed)
    print(motor)
    
    cv2.imshow("Capture", contour)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
  
     
#img.release()
#cv2.destroyAllWindows()