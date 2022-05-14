import cv2
import numpy as np

#----Create a kernel
kernel = np.ones((5,5), np.uint8) ## ---> Create a matrix 5x5
print("Package Imported")
img = cv2.imread("Resources\car.jpg")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray,(7,7),0)
img_canny = cv2.Canny(img, 100,100) ##----> Show Image edges () (modify 120,100) -->increase 120 reduce the edges
img_dilation = cv2.dilate(img_canny, kernel, iterations=1) ##---> Because edges not aligned properly, we can use dilation to increase the edge thickness. Increase iterations value to increase thickness
img_erosion = cv2.erode(img_dilation, kernel, iterations=1) ## ---> Opposite of Dilation. Reduce the edge thickness

cv2.imshow("Gray", img_gray)
cv2.imshow("Blur", img_blur)
cv2.imshow("Canny", img_canny)
cv2.imshow("Dialation", img_dilation)
cv2.imshow("Erosion", img_erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()