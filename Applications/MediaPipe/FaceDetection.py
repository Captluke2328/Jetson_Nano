import cv2
import mediapipe as mp
import time

mFace = mp.solutions.face_detection
#face = mFace.FaceDetection()
mpDraw = mp.solutions.drawing_utils

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
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

def show_camera():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    with mFace.FaceDetection(min_detection_confidence=0.5) as face:
        while True:
            success,img = cap.read()
            img.flags.writeable = True
            
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face.process(imgRGB)

            if results.detections:
                for detections in results.detections:
                    for id, lm in enumerate(results.detections):
                        h, w, c = img.shape
                        cv2.line(img, (w//2, 0), (w//2, h), (0, 255, 0), 3)
                    mpDraw.draw_detection(img, detections)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)),(10,60), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),4)
            cv2.imshow("Results",img)

            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
           
if __name__ == "__main__":
    show_camera()
    
