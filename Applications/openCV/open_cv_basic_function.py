import cv2

img = cv2.imread("/home/pi/Desktop/Project/opencv_project/resources/pi_black_glow2.jpg")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#Display image categories
cv2.imshow("Original Image", img)
cv2.imshow("Gray Image", imgGray)

cv2.waitKey(0)
