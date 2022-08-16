#!/usr/bin/env python3


from tkinter.ttk import Frame
import jetson.inference
import jetson.utils
import argparse
import sys

import numpy as np
from video_capture import *

parser = argparse.ArgumentParser(description="Run pose estimation DNN on a video/image stream.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.poseNet.Usage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="resnet18-body", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="links,keypoints", help="pose overlay flags (e.g. --overlay=links,keypoints)\nvalid combinations are:  'links', 'keypoints', 'boxes', 'none'")
parser.add_argument("--threshold", type=float, default=0.15, help="minimum detection threshold to use") 

try:
	opt = parser.parse_known_args()[0]
except:
	#print("")
	parser.print_help()
	sys.exit(0)
 
gstream_pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int){capture_width:d}, height=(int){capture_height:d}, "
    "format=(string)NV12, framerate=(fraction){framerate:d}/1 ! "
    "nvvidconv flip-method={flip_method:d} ! "
    "video/x-raw, width=(int){display_width:d}, height=(int){display_height:d}, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink".format(
        capture_width=1280,
        capture_height=720,
        framerate=60,
        flip_method=2,
        display_width=1280,
        display_height=720,
    )
)

cam = VideoCapture(gstream_pipeline,cv2.CAP_GSTREAMER)
net = jetson.inference.poseNet(opt.network, sys.argv, opt.threshold)

while True:
    
    ret,frame= cam.read()
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    
    #Convert numpy ndarray into CUDA memory to pass to the detector
    img = jetson.utils.cudaFromNumpy(frame_rgba)

    poses = net.Process(img, overlay=opt.overlay)
    for pose in poses:
        #print(f"pose) : {pose}")
        #print(f"keypoints : {pose.Keypoints}")
        #print(f"Links : {pose.Links}")

        dictLinks = pose.Links
        dictPoint = pose.Keypoints
        x = 0
        y = 0
        x2 = 0
        y2 = 0
        
        for tup in pose.Links:
            #print(tup)
            #print(tup[0])
            #print(tup[1])
            a = dictPoint[tup[0]]
            ase = dictPoint[tup[1]]
            #print(a, ase)
            x = getattr(a,"x")
            y = getattr(a,"y")
            x2 = getattr(ase,"x")
            y2 = getattr(ase,"y")
            cv2.line(frame, (round(x),  round(y)),(round(x2), round(y2)), (0,255,0),2)
            cv2.circle(frame, (round(x),  round(y)), 5, (0, 0, 255), cv2.FILLED)

        left_wrist_idx = pose.FindKeypoint('left_wrist')
        left_shoulder_idx = pose.FindKeypoint('left_shoulder')
        right_wrist_idx = pose.FindKeypoint('right_wrist')
        right_shoulder_idx = pose.FindKeypoint('right_shoulder')
        
        if left_wrist_idx < 0 or left_shoulder_idx <0:
            continue
        
        if right_wrist_idx < 0 or right_shoulder_idx <0:
            continue

        left_wrist = pose.Keypoints[left_wrist_idx]
        left_shoulder = pose.Keypoints[left_shoulder_idx]
        right_wrist = pose.Keypoints[right_wrist_idx]
        right_shoulder = pose.Keypoints[right_shoulder_idx]
        
        # point_x = left_shoulder.x - left_wrist.x 
        # point_y = left_shoulder.y - left_wrist.y
        
        #print(f"person {pose.ID} is pointing towards ({point_x}, {point_y})")
        #print(f"keypoints {left_wrist}, {left_shoulder}, {right_wrist}, {right_shoulder}")
        #print(f"left_wrist_id :  {left_wrist_idx}  left_shoulder_id : {left_shoulder_idx}")

        if (left_wrist.y < left_shoulder.y) and (right_wrist.y > right_shoulder.y):
            print("Move left")
            
        if (right_wrist.y < right_shoulder.y) and (left_wrist.y > left_shoulder.y):
            print("Move Right")
            
    cv2.imshow("Output",  frame )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        SystemExit(0)
        
cv2.destroyAllWindows()
    
