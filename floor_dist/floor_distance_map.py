import os
import cv2
import numpy as np

DIR = "floor_dist/floor_benny/depth/"

low, high = 40, 200

final = cv2.imread(DIR + "d0.jpg", cv2.IMREAD_GRAYSCALE)

w, h = final.shape[1], final.shape[0]

mask = cv2.inRange(final, low, high)
final = cv2.bitwise_and(final, mask)

for filename in os.listdir(DIR):
    img = cv2.imread(DIR + filename,  cv2.IMREAD_GRAYSCALE)

    mask = cv2.inRange(img, low, high)
    img = cv2.bitwise_and(img, mask)

    final = np.maximum(final, img)

vertices = np.array(
            [[0, 200],
             [w, 200],
             [w, h],
             [0, h]])

mask = np.zeros_like(final)
cv2.fillPoly(mask, np.int32([vertices]), 255)
final = cv2.bitwise_and(final, mask)

# final = cv2.medianBlur(final, 9)

cv2.imshow("floor", final)

# cv2.imwrite("floor_dist/floor_dist_benny.jpg", final)

cv2.waitKey(0)