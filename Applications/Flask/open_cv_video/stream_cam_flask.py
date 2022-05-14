from flask import Flask, Response, render_template
import cv2  
import threading
from time import sleep
import os


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! " ##! appsink
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

global cam
cam = None

global frame_cap
frame_cap = None
#GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'
#cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#gstreamer_pipe = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'
#gstreamer_vl4 = ('v4l2src device=/dev/video{} ! video/x-raw, width=(int){}, height=(int){} ! videoconvert ! appsink').format(0, 640, 480)
#gstreamer_nvarg = ('nvarguscamerasrc ! video/x-raw(memory:NVMM),width=640, height=480, framerate=21/1, format=NV12 ! nvvidconv flip-method=0 ! video/x-raw,width=960, height=616 ! nvvidconv ! video/x-raw ! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert ! appsink name=sink max-buffers=5')
#cam = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
#cam = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert !  video/x-raw, format=(string)BGR ! appsink')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def read_cam():
    #global cam
    global frame_cap
    cams = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    while True and cams.isOpened():
        success, frame_cap = cams.read()
        if not success:
            break

        #cam = frame_cap.copy()

    cams.release()
    cv2.destroyAllWindows()
    os.system('sudo systemctl restart nvargus-daemon')

def encode_cam():
    while True:
        #global cam
        if frame_cap is None:
            continue
        success, encoded_image = cv2.imencode('.jpg', frame_cap)
        frame = encoded_image.tobytes()

        if not success:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(encode_cam(),
                     mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    process_thread = threading.Thread(target=read_cam)
    process_thread.daemon = True

    process_thread.start()
    app.run(host='0.0.0.0', port=80, threaded=True)


    