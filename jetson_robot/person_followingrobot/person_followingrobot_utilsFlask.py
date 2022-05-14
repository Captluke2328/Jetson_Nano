from person_followingrobot_function import *
from csi_camera import CSI_Camera
from flask import Flask, Response, render_template
from PIL import Image
import threading
import os
import time
import copy

timeStamp=time.time()

fpsFilt=0
show_fps = True

os.system ('sudo systemctl restart nvargus-daemon')
pError =0
pid =[0.5,0.4]

#camera = initializecamera()

# Frame sent to Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock
thread_lock = threading.Lock()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def readcam():
    global video_frame,thread_lock
    camera = initializecamera()
    while True:

        #Step 1     
        img,info = captureimage(camera)    
        #img = cv2.resize(img, (0,0), None, 2,2)
        #print(info[0][0])

        #Step 2
        draw = drawOverlays(img, fpsFilt)
        
        #Step 3
        #img, perror = trackobject(img,info,pid,pError)
        #thread = threading.Thread(target= trackobject, args = (img,info,pid,pError))
        #thread.start()
        
        with thread_lock:
            video_frame = img.copy()  
    
def encode_cam():
    global thread_lock
    while True:
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            success, encoded_image = cv2.imencode('.jpg', video_frame)
            frame = encoded_image.tobytes()
            if not success:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(encode_cam(),
                     mimetype = 'multipart/x-mixed-replace; boundary=frame')
    
   
if __name__ == '__main__':
    #Start Time to count FPS
    
    dt=time.time()-timeStamp
    timeStamp=time.time()
    fps=1/dt
    fpsFilt=.9*fpsFilt + .1*fps
    #FPSvalue = copy.copy(fpsFilt)
    process_thread = threading.Thread(target= readcam)
    process_thread.daemon = True
    process_thread.start()
    #app.run(host='10.60.130.138', threaded=True)
    app.run(host='192.168.8.121', threaded=True)
