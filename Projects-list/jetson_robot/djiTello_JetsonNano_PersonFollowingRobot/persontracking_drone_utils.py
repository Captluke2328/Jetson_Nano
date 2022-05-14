import os
from persontracking_drone_function import *
#from persontracking_drone_camera_udp import *
from time import sleep
from djitellopy import tello
import cv2
import socket
import threading

tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)
VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111
cap = None
response = None
socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
socket.bind (('', tello_port))

def run_udp_receiver ():
    while True:
        try:
            response, _ = socket.recvfrom (1024)
        except Exception as e:
            print (e)
            break
thread = threading.Thread (target = run_udp_receiver, args = ())
thread.daemon = True
thread.start ()
socket.sendto ('command'.encode (' utf-8 '), tello_address)
# take off
socket.sendto ('streamon'.encode (' utf-8 '), tello_address)
udp_video_address = 'udp://@' + str(VS_UDP_IP) + ':' + str (VS_UDP_PORT)

if cap is None:
    cap = cv2.VideoCapture (udp_video_address)
if not cap.isOpened ():
    cap.open (udp_video_address)


#os.system('sudo systemctl restart nvargus-daemon')

startCounter=0

#myDrone = initializeTello()

pError=0
pid =[0.2,0.2]
#W,H = 970,720
W,H = 640,480


while True:
    # Flight
    #if startCounter == 0:
        #myDrone.takeoff()
    #    startCounter=1
        
    # Step 1
    #img = captureimage(myDrone, W, H)
    #img = main()
    ret, img = cap.read()

    # Step  2
    info = findingmage(img, W)
    
    # Step 3
    #draw = drawOverlays(img, W, H)
    
    # Step 3
    #if info !=None:
    #    cx = info[0][0]
    #    img, pError = trackobject(img, cx,pid,pError,myDrone, W)
    #else:
        #img, pError = trackobject(img, 0,pid,pError, myDrone, 0)

    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        #myDrone.land()
        sleep(1)
        break
        
        
