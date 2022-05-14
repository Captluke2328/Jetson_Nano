from person_followingrobot_function import *
from flask import Flask, Response, render_template
from PIL import Image
import threading
import os
import time

timeStamp=time.time()
fpsFilt=0
show_fps = True

#os.system ('sudo systemctl restart nvargus-daemon')
pError =0
pid =[0.5,0.4]

camera = initializecamera()

if __name__ == '__main__':     
    while True:       
        #Start Time to count FPS
        dt=time.time()-timeStamp
        timeStamp=time.time()
        fps=1/dt
        fpsFilt=.9*fpsFilt + .1*fps

        #Step 1
        img,info = captureimage(camera)
        
        #img = cv2.resize(img, (0,0), None, 2,2)
        #print(info[0][0])

        #Step 2
        draw = drawOverlays(img, fpsFilt)
        
        #Step 3
        #thread = threading.Thread(target= trackobject, args = (img,info,pid,pError))
        #thread.start()
        img, pError = trackobject(img,info,pid,pError)
            
        cv2.imshow("Frame",img)
        if cv2.waitKey(1) & 0XFF==ord('q'):
            break

    camera.stop()
    cv2.destroyAllWindows()
