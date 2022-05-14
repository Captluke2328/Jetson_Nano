from flask import Flask, Response, render_template
from PIL import Image
import threading
import cv2
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
        "videoconvert ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# Frame sent to Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock
thread_lock = threading.Lock()

# Tolerance Value
tolerance = 0.1

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def captureFrames():
    global video_frame, thread_lock
    cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    while True and cam.isOpened():
        ret, frame = cam.read()
        
        if not ret:
            break

        # with thread safe access and copy the frame into global variables
        with thread_lock:
            video_frame = frame.copy()

    cam.release()
    cv2.destroyAllWindows()
    os.system('sudo systemctl restart nvargus-daemon')

def encodeFrame():
    global thread_lock
    while True:
        # retrieve thread_lock to access the global video_frame object contain
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            cv2_im = video_frame
            cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            cv2_im = draw_overlays(cv2_im)
            ret, encoded_image = cv2.imencode('.jpg', cv2_im)
            frame = encoded_image.tobytes()
            if not ret:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def draw_overlays(cv2_im):
    height, width, channels = cv2_im.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    global tolerance
    print(height, width)
    
    # Top
    cv2_im = cv2.rectangle(cv2_im, (0,0), (width,24), (0,0,0), -1)

    # Bottom
    cv2_im = cv2.rectangle(cv2_im, (0, height-24), (width,height), (0,0,0), -1)

    # Center Cross Lines
    cv2_im = cv2.rectangle(cv2_im, (0, int(height/2)-1), (width, int(height/2)+1), (255,0,0),-1) ## Vertical
    cv2_im = cv2.rectangle(cv2_im, (int(width/2)-1,0), (int(width/2)+1, height), (255,0,0), -1) ## Horizontal

    # Write tolerance
    str_tol = 'Tol : {}'.format(tolerance)
    cv2_im = cv2.putText(cv2_im, str_tol, (10,height-8), font, 0.55, (155,150,255),2)

    # Width and Height
    text_dur = 'Width : {} Height: {}'.format(width,height)
    cv2_im = cv2.putText(cv2_im, text_dur, (10,16), font, 0.55, (150,150,255), 1)

    # Tolerance Box
    cv2_im = cv2.rectangle(cv2_im, (int(width/2-tolerance*width), int(height/2-tolerance*height)), (int(width/2+tolerance*width), int(height/2+tolerance*height)), (0,255,0),2)

    return cv2_im
    
@app.route('/video_feed')
def video_feed():
    return Response(encodeFrame(),
                     mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True
    process_thread.start()
    app.run(host='0.0.0.0', port=80, threaded=True)
    
