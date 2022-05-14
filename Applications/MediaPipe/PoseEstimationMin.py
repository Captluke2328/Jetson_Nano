import cv2
import mediapipe as mp
import time

mPose = mp.solutions.pose
pose = mPose.Pose()
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
    
    while True: 
        success,img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            lmList = []
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id,lm)
                lmList.append([id,cx,cy])
                print(lmList[0], w,h)
                
                cv2.circle(img, (cx,cy),5, (255,0,0), 4)
            mpDraw.draw_landmarks(img, results.pose_landmarks, mPose.POSE_CONNECTIONS)
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(10,60), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),4)
        cv2.imshow("Results",img)

        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
           
if __name__ == "__main__":
    show_camera()
    