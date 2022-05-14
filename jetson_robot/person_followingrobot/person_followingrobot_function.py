#!/usr/bin/python3

import jetson.inference
import jetson.utils
import cv2
import numpy as np
from csi_camera import CSI_Camera
import SerialModule as sm
import os
os.system ('sudo systemctl restart nvargus-daemon')

font=cv2.FONT_HERSHEY_SIMPLEX
DISPLAY_WIDTH=640
DISPLAY_HEIGHT=320
SENSOR_MODE_720=3

ser = sm.initConnection('/dev/ttyACM0',9600)
net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)

def drawOverlays(img, fpsFilt):
    # Draw black rectangle bottom
    cv2.rectangle(img, (0, DISPLAY_HEIGHT-24), (DISPLAY_WIDTH,DISPLAY_HEIGHT), (0,0,0), -1)
    
    # Draw center middle line
    cv2.line(img,(DISPLAY_WIDTH//2,0),(DISPLAY_WIDTH//2,DISPLAY_HEIGHT-24), (255,0,255),3) # 255,0,255
    
    # FPS Counter
    #fps_text = 'FPS : {}'.format(str(round(fpsFilt,1)))
    #cv2.putText(img,fps_text,(10,DISPLAY_HEIGHT- 8),font,0.5,(150,150,255),2)
    return img

def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    #if display_fps:
        #text_dur = 'FPS : {}'.format(str(csi_camera.last_frames_displayed))
        #cv2.putText(camera_image, str(csi_camera.last_frames_read), (10,16), font, 0.55, (150,150,255), 1)  
    return camera_image 

def trackobject(img, info,pid,pErr0r):
    if int(info[1]) !=0 and int(info[1]) < 80000 :
        error = DISPLAY_WIDTH//2 - info[0][0]
        posX = int(pid[0]*error + pid[1]*(error-pErr0r))
        posX = int(np.interp(posX, [-DISPLAY_WIDTH//4, DISPLAY_WIDTH//4], [-35,35]))
        pErr0r = error
        print(str(posX) + " " + str(info[1]))
        sm.sendData(ser, [50,posX],4)
    
    elif int(info[1]) > 80000:
        sm.sendData(ser, [0,0],4)
        print("Reverse")
    else:
        sm.sendData(ser,[0,0],4)
        print("Not Object Found")

    return img, pErr0r

def initializecamera():
    left_camera = CSI_Camera()
    left_camera.create_gstreamer_pipeline(
        sensor_id=0,
        sensor_mode=SENSOR_MODE_720,
        framerate=30,
        flip_method=0,
        display_height=DISPLAY_HEIGHT,
        display_width=DISPLAY_WIDTH,
    )
    left_camera.open(left_camera.gstreamer_pipeline)
    left_camera.start()
    
    if (not left_camera.video_capture.isOpened()):
        print("Unable to open any cameras")
        SystemExit(0)
    
    return left_camera
    
def captureimage(left_camera):
    while True:    
        #try:
        myobjectListC = []
        myobjectListArea = []
        img = read_camera(left_camera,True)
        height = img.shape[0]
        width = img.shape[1]
        frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
        frame=jetson.utils.cudaFromNumpy(frame)
        value = 0    
        detections = net.Detect(frame, width, height)
        for detect in detections:
            ID=detect.ClassID
            top=int(detect.Top)
            left=int(detect.Left)
            bottom=int(detect.Bottom)
            right=int(detect.Right)
            #widths = detection.Width
            area = int(detect.Area)
            location = detect.Center
            item=net.GetClassDesc(ID)
            
            cx = location[0]
            cy = location[1]
            myobjectListArea.append(area)
            myobjectListC.append([cx,cy])
            
        #print(item)
        if len(myobjectListArea) !=0:
            if ID==1:
                cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),3)
                cv2.line(img, (DISPLAY_WIDTH//2, int(cy)), (int(cx),int(cy)), (255,0,255),3)
                cv2.putText(img,item,(left,top+20),font,.95,(248, 254, 0),3)
                i = myobjectListArea.index(max(myobjectListArea))
                return img, [myobjectListC[i],myobjectListArea[i]]
        else:
            return img, [[0,0],0]
       # return img, [[0,0],0]  
       # except:
       #     print("Could not read image from camera")
        
          
if __name__ == "__main__":
    camera = initializecamera()
    while True:   
        img = captureimage(camera)
           
        cv2.imshow("Frame",img)
        if cv2.waitKey(1) & 0XFF==ord('q'):
            break
    camera.stop()
    cv2.destroyAllWindows()


    
