import cv2
import threading
from flask import Flask, Response, render_template
import os

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def captureFrames():
    global cam
    cams = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    while True and cams.isOpened():
        return_key, frame = cams.read()
        if not return_key:
            break

        cam = frame.copy()

    cams.release()
    cv2.destroyAllWindows()
    os.system('sudo systemctl restart nvargus-daemon')

def encodeFrame():
    while True:
        global cam
        if cam is None:
            continue
        return_key, encoded_image = cv2.imencode('.jpg', cam)
        frame = encoded_image.tobytes()

        if not return_key:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(encodeFrame(),
                     mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    process_thread.start()
    app.run(host='0.0.0.0', port=80, threaded=True)
