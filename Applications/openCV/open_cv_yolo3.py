import cv2
import numpy as np

cap = cv2.VideoCapture(0)
whT = 320 #- Width High Target. We are using 320 yolo
confThreshold = 0.5
nms_threshold = 0.3  # The lower is more aggresive and less number of boxes. Can reduce the boxes

classesFile = r'/home/jlukas/Desktop/My_Project/Resources/mobilenet_ssd/coco.names'
classNames = []

#---- Read the Coco Name files contents---
with open (classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

print(classNames)
print(len(classNames))

modelConfiguration = r'/home/jlukas/Desktop/My_Project/Resources/mobilenet_ssd/yolov3-tiny.cfg'
modelWeights = r'/home/jlukas/Desktop/My_Project/Resources/mobilenet_ssd/yolov3-tiny.weights'

#--- Create our network--
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = [] ## --> Will contain width and height
    classIds = [] ## --> Will contain classIds
    confidenceLevel = [] ## --> When we find good value. We will store it here

    for output in outputs:
        for det in output:
            scores = det[5:] # We will first remove the first 5 elements from result and find the highest values
            classId = np.argmax(scores) ## --> find index of maximum values
            confidence = scores[classId]  ## --> Store the highest index into confidence

            if confidence > confThreshold: # If above 50 percent then save it
                w,h = int(det[2]*wT), int(det[3]*hT) ## -- Refer to image from this tutorial to determine X & Y index
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2) ## Access to the table 300X 85
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confidenceLevel.append(float(confidence))

    #print(len(bbox))

    # ---- To remove double bounding box --
    indices = cv2.dnn.NMSBoxes(bbox,confidenceLevel,confThreshold,nms_threshold)
    #print(indices)
    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        #print(x,y,w,h)
        cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confidenceLevel[i]*100)}%',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


while True:
    success, img = cap.read()

    #---Create our Capture image to Blob because network recognize it as Blob. Set Blob as an input to our network
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0],1,crop=False )
    net.setInput(blob)
    
    # -- Get the name of  the all layer detected from webcam --
    LayerNames = net.getLayerNames()
    #print(LayerNames)

    # -- We wanted to get the first element and subract -1 from it. For example 200 - 1 
    outputNames = [LayerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames) # --> THis is output name of our layers that return 2 outputs yolo_16, yolo_23

    # -- Return the indices of the output layers. We can use this index from result 
    #print(net.getUnconnectedOutLayers())

    outputs = net.forward((outputNames))
    #print(len(outputNames)) # ---> We are getting 3 output number from OutputNames
    #print(outputs[0].shape) # ---> outputs will be in list (300 rows and 85 Columns)
    #print(outputs[1].shape) #---->(1200, 85). 1200 is bounding boxe, 85  (5)represent Width & Height & Centre x, Centre y
    #print(outputs[2].shape) #---->(4800, 85)
    #print(outputs[0][0]) # --- > read the first row from Boxes for outputs 0. We will go through each of the outputs
 
    findObjects(outputs, img)

    cv2.imshow('Image', img)
    cv2.waitKey(1)


