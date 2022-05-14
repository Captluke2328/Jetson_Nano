#!/usr/bin/python3
import jetson.inference
import jetson.utils
import serial
from time import sleep

global flag
flag = 0

image_width = 1640
image_height = 720

center_image_x = image_width / 2
center_image_y = image_height / 2

minimum_area = 2500
maximum_area = 180000

object_area = 0

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1640,720,"csi://0")

display = jetson.utils.glDisplay()
with serial.Serial('/dev/ttyACM0',9600,timeout=10) as ser:
    while display.IsOpen():
        img, width, height = camera.CaptureRGBA()
        detections = net.Detect(img, width, height)
        for detection in detections:
            label = net.GetClassDesc(detection.ClassID)
            widths = detection.Width
            heights = detection.Height
            area = detection.Area
            location = detection.Center
            if (label == "person"):
                #print("label :" + label + "\n" + "widths :" + str(widths) + "\n" + "height :" + str(height) + "\n" + "area :" +  str(area) + "\n" + "center :" + str(location) + "\n")
                #if object_area < area:
                #    object_area = area
                #    object_x = location[0]
                #    object_y = location[1]
                    
                #if object_area > 0:
                ball_location = [area, location[0], location[1]]
                print("area :" + str(ball_location[0]) + "\n" + "object_x :" + str(ball_location[1]) + "\n" + "object_y :" + str(ball_location[2]) + "\n")
                if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area ):
                    if ball_location[1] > (center_image_x + (image_width/7)):
                        print("Turning right")
                        ser.write(bytes('L\n', 'utf-8'))
                        #ser.write(bytes('Z\n', 'utf-8'))

                    elif ball_location[1] < (center_image_x - (image_width/7)):
                        print("Turning left")
                        ser.write(bytes('R\n', 'utf-8'))
                        #ser.write(bytes('X\n', 'utf-8'))
                      
                    else:
                        print("Forward")
                        ser.write(bytes('F\n', 'utf-8'))
                                         
                #elif (ball_location[0] > maximum_area):
                #    print("Left")
                #    ser.write(bytes('S\n', 'utf-8'))
                    
                else:
                    print("Stop")
                    ser.write(bytes('S\n', 'utf-8'))
                                                     
            #elif (flag == 1) :
            #    print("Lefts")
            #    flag = 0
            #    ser.write(bytes('Q\n', 'utf-8'))
                        
            # if ball_location:
            #     if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
            #         if ball_location[1] > (center_image_x + (image_width/3)):
            #             print("Turning right")
            #         elif ball_location[1] < (center_image_x - (image_width/3)):
            #             print("Turning left")
            #         else:
            #             print("Forward")
            #else:
            #    ser.write(bytes('Q\n', 'utf-8'))
                        
        display.RenderOnce(img, width, height)
        display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        

