import cv2
import sys
import time
from threading import Thread

cv2_im = cv2.imread(r'/home/jlukas/Desktop/My_Project/Resources/opamp.jpg')
def main():
    height=480
    width=640
    tolerance=1
    height, width = cv2_im.shape
    font=cv2.FONT_HERSHEY_SIMPLEX

    #draw black rectange on top
    cv2_im = cv2.rectangle(cv2_im, (0,0), (width, 24), (0,0,0), -1)
    #return cv2_im


if __name__ == '__main__':
    main()
