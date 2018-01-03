import numpy as np
import cv2

cv2.ocl.setUseOpenCL(False)

LowerBound = np.array([150, 50, 100])
UpperBound = np.array([200, 255, 255])

def filter_image_by_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LowerBound, UpperBound)
    return mask