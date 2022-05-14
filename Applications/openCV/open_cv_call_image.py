import cv2
import numpy as np

print("Package Imported")
img = cv2.imread('E:\Python Project\Resources\car.jpg')

cv2.imshow("car", img)
cv2.waitKey(0)
cv2.destroyAllWindows()