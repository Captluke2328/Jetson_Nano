import socket
import threading
import cv2

tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)

VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111

cap = None
response = None
socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
socket.bind (('', tello_port))

def run_udp_receiver ():
    while True:
        try:
            response, _ = socket.recvfrom (1024)
        except Exception as e:
            print (e)
            break
thread = threading.Thread (target = run_udp_receiver, args = ())
thread.daemon = True
thread.start ()

socket.sendto ('streamon'.encode (' utf-8 '), tello_address)
udp_video_address = 'udp://@' + str(VS_UDP_IP) + ':' + str (VS_UDP_PORT)

if cap is None:
    cap = cv2.VideoCapture (udp_video_address)
    
if not cap.isOpened():
    cap.open(udp_video_address)

while True:
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
