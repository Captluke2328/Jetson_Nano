import cv2  
from flask import Flask, render_template, Response
from threading import Thread
import time
import socket
import io

app = Flask(__name__)
#cam = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert !  video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)
#cam = cv2.VideoCapture('/dev/video0')
#test = 'v4l2src device=/dev/video0 name=e ! video/x-raw, width=640, height=480 ! videoconvert ! video/x-raw, width=640, height=480, format=(string)YUY2 ! xvimagesink'
#tests = ('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink')

#vc = cv2.VideoCapture(0)

class WebcamVideoStream:
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

vc = WebcamVideoStream(src=0).start()
time.sleep(1.0)

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

def gen(vc):
    """Video streaming generator function."""
    while True:
        frames = vc.read()
        ret, jpeg = cv2.imencode('.jpg', frames)
        frame = jpeg.tobytes()
        #cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    #global vc
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(vc),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, threaded=True)
               