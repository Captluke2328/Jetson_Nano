import cv2
import jetson.utils
import jetson.inference
import numpy as np
from video_capture import *

model = jetson.inference.detectNet("SSD-Mobilenet-v2")
width = 640
height = 320

CAM_ASPECT_RATIO = 16.0 / 9.0
INPUT_IMG_SIZE = 224

gstream_pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int){capture_width:d}, height=(int){capture_height:d}, "
    "format=(string)NV12, framerate=(fraction){framerate:d}/1 ! "
    "nvvidconv top={crop_top:d} bottom={crop_bottom:d} left={crop_left:d} right={crop_right:d} flip-method={flip_method:d} ! "
    "video/x-raw, width=(int){display_width:d}, height=(int){display_height:d}, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink".format(
        capture_width=int(INPUT_IMG_SIZE * CAM_ASPECT_RATIO),
        capture_height=INPUT_IMG_SIZE,
        framerate=60,
        crop_top=0,
        crop_bottom=INPUT_IMG_SIZE,
        crop_left=int(INPUT_IMG_SIZE * (CAM_ASPECT_RATIO - 1) / 2),
        crop_right=int(INPUT_IMG_SIZE * (CAM_ASPECT_RATIO + 1) / 2),
        flip_method=0,
        display_width=INPUT_IMG_SIZE,
        display_height=INPUT_IMG_SIZE,
    )
)

cam = VideoCapture(gstream_pipeline,cv2.CAP_GSTREAMER)

# Opening the camera
while True:

    ret, frame = cam.read()
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    
    #Convert numpy ndarray into CUDA memory to pass to the detector
    img = jetson.utils.cudaFromNumpy(frame_rgba)
    
    detections = model.Detect(img, width, height, "box,labels,conf")
    
    #Convert CUDA memory to numpy
    conv1 = jetson.utils.cudaToNumpy(img, width, height, 4)        
    conv2 = cv2.cvtColor(conv1, cv2.COLOR_RGBA2RGB).astype(np.uint8)
    conv3 = cv2.cvtColor(conv2, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", conv3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        SystemExit(0)

cam.release()
cv2.destroyAllWindows()