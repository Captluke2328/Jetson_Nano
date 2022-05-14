import cv2
import numpy as np

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int)%d, height=(int)%d, "
    "format=(string)NV12, framerate=(fraction)%d/1 ! "
    "nvvidconv flip-method=%d ! "
    "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
    % (
        capture_width,
        capture_height,
        framerate,
        flip_method,
        display_width,
        display_height,
    )
)

cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

#cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert !  video/x-raw, format=(string)BGR ! appsink')

whT = 320
confThreshold = 0.5
nms_threshold = 0.3

classesFile = '/home/jlukas/Desktop/My_Project/Resources/yolo_v3/coco.names'
classNames = []

#---Read the coco names file contents---
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').rsplit('\n')

#---Initialize the Yolo_v3_tiny file---
modelConfiguration = '/home/jlukas/Desktop/My_Project/Resources/yolo_v3/yolov3-tiny.cfg'
modelWeights = '/home/jlukas/Desktop/My_Project/Resources/yolo_v3/yolov3-tiny.weights'

#---Create our Network---
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    boundingbox = []
    classIds = []
    confidenceLevel = []

    for output in outputs:
        for detect in output:
            scores = detect[5:] # Will first remove the first 5 elements from output
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence > confThreshold:
                w,h = int(detect[2]*wT), int(detect[3]*hT) 
                x,y = int ((detect[0]*wT)- w/2), int((detect[1]*hT - h/2)) 
                boundingbox.append([x,y,w,h])
                classIds.append(classId)
                confidenceLevel.append(float(confidence))
    #print(len(boundingbox))

    indices = cv2.dnn.NMSBoxes(boundingbox,confidenceLevel,confThreshold,nms_threshold)
    #print(indices)
    for i in indices:
        i = i[0]
        box = boundingbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        #print(x,y,w,h)
        cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confidenceLevel[i]*100)}%',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        if (f'{classNames[classIds[i]].upper()}') == 'PERSON':
            print("This is person")
        else:
            print("This is not person")

  

while True:
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():     
        success, img = cap.read()
    
        #---Create our Capture Image to Blob because network recognize it as a Blob. We set Blob as an input to our network
        blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,1],1,crop=False)
        net.setInput(blob)
        #print(blob)

        #---Get the name of the all layer detected from webcam---
        LayerNames = net.getLayerNames()
        #print(Layernames)
    
        #---Return the indices of the output layers. We can use index later to extract the output
        #print(net.getUnconnectedOutLayers())

        #---We wanted tp get the first element and subtract -1 from it. For example 200 -1
        outputNames = [LayerNames[i[0]-1] for i in net.getUnconnectedOutLayers()] 
        #print(outputNames)
    
        outputs = net.forward(outputNames)
        #print(outputs)
        #print(outputs[0].shape) ##---> Outputs will be list (300 rows and 85 columns)
        #print(outputs[1].shape) ##---> Outputs will be list (1200 rows and 85 columns)
        #print(outputs[3].shape) ##---> Outputs will be list (4800 rows and 85 columns)
        #print(outputs[0][0])  ##---> read the first row from Boxes for outputs 0 (300 rows and 85 columns)
    
        findObjects(outputs,img)
    
        cv2.imshow("Captured Data", img)
        cv2.waitKey(3)


