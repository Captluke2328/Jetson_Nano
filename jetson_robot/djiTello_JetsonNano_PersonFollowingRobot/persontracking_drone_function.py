import jetson.inference
import jetson.utils
from djitellopy import Tello
import cv2
import numpy as np
import os

#os.system ('sudo systemctl restart nvargus-daemon')
font=cv2.FONT_HERSHEY_SIMPLEX
DISPLAY_WIDTH=640
DISPLAY_HEIGHT=480

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def drawOverlays(img, W, H):
    #height = img.shape[0]
    #width = img.shape[1]
    #cv2.line(img,(width//2,0),(width//2,height), (255,0,255),3) # 255,0,255

    cv2.line(img,(W//2,0),(W//2,H), (255,0,255),3) # 255,0,255
    return img
    
def captureimage(img, W, H):
    myFrame = img.get_frame_read()
    #height, width, _ = myFrame.shape
    
    #new_h = int(720/2)
    #new_w = int(960/2)
    
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(W,H))
    
    return img

def findingmage(img, W):
    myobjectListC = []
    myobjectListArea = []    
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
        area = int(detect.Area)
        location = detect.Center
        item=net.GetClassDesc(ID)
        
        cx = location[0]
        cy = location[1]
        print(str(cy) + " height")
        myobjectListArea.append(area)
        myobjectListC.append([cx,cy])
        
    if len(myobjectListArea) !=0:
        if ID==1:
            #print(width, height)
            cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),3)
            cv2.line(img, (W//2, int(cy)), (int(cx),int(cy)), (255,0,255),3)
            cv2.putText(img,item,(left,top+20),font,.95,(248, 254, 0),3)
            i = myobjectListArea.index(max(myobjectListArea))
            return [myobjectListC[i],myobjectListArea[i]]
        else:
            return [[0,0],0]
    else:
        return [[0,0],0]
        
def trackobject(img, cx,pid,pError,myDrone, W): 
    error = cx - (W//2+int(330))
    print(error, cx, W//2)
    speed = pid[0]*error + pid[1]*(error-pError)
    #posX = int(np.interp(posX, [-DISPLAY_WIDTH//4, DISPLAY_WIDTH//4], [-35,35]))
    #pErr0r = error
    speed = int(np.clip(speed,-40,40))
    
    if cx !=0 :
        myDrone.yaw_velocity = speed
        #print(str(posX) + " " + str(info[1]))
    
    #elif int(info[1]) > 80000:
        #sm.sendData(ser, [0,0],4)
    #    print("Reverse")
    
    else:
        print("Not Object Found")
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
        
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
        
    return img, speed
    
    
            
    
    
    
    
