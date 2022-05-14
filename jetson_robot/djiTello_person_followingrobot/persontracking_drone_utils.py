import os
from persontracking_drone_function import *
from time import sleep
from djitellopy import tello

os.system('sudo systemctl restart nvargus-daemon')

startCounter=0

myDrone = initializeTello()

pError=0
pid =[0.2,0.2]
W,H = 640,480
#W,H = 480,360

if __name__ == '__main__':
    while True:
        # Flight
        if startCounter == 0:
           # myDrone.takeoff()
            startCounter=1
            
        # Step 1
        img = captureimage(myDrone, W, H)
        
        # Step  2
        info = findingmage(img, W)
        
        # Step 3
        draw = drawOverlays(img)
        
        # Step 3
        if info !=None:
            cx = info[0][0]
            pError = trackobject(cx,pid,pError,myDrone, W)
        else:
            pError = trackobject(0,pid,pError, myDrone, 0)

        cv2.imshow("Tracking",img)
        if cv2.waitKey(1) & 0XFF==ord('q'):
            myDrone.land()
            sleep(1)
            break
        
        