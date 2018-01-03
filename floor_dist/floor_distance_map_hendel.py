import os
import cv2
import numpy as np

DIR = "floor_dist/floor_benny/depth/"
DIR_2 = "floor_dist/floor/depth/"

low, high = 40, 220

img = cv2.imread(DIR + "d0.jpg", cv2.IMREAD_GRAYSCALE)
# img[img == 0] = 1
imgs = np.array([img])


w, h = img.shape[1], img.shape[0]

mask = cv2.inRange(img, low, high)
img = cv2.bitwise_and(img, mask)

for filename in os.listdir(DIR):
    img = cv2.imread(DIR + filename, cv2.IMREAD_GRAYSCALE)

    mask = cv2.inRange(img, low, high)
    img = cv2.bitwise_and(img, mask)

    imgs = np.append(imgs, [img], axis=0)

for filename in os.listdir(DIR_2):
    img = cv2.imread(DIR_2 + filename, cv2.IMREAD_GRAYSCALE)

    mask = cv2.inRange(img, low, high)
    img = cv2.bitwise_and(img, mask)

    imgs = np.append(imgs, [img], axis=0)

# imgs = imgs.astype('float')

# imgs[imgs == 0] = np.nan

final = np.max(imgs, axis=0)

# final = np.nanmedian(imgs, axis=0)

final = cv2.medianBlur(final, 19)

# final = final / 255

vertices = np.array(
            [[0, 310],
             [w, 310],
             [w, h],
             [0, h]])

mask = np.zeros_like(final)
cv2.fillPoly(mask, np.int32([vertices]), 255)
final = cv2.bitwise_and(final, mask)

print(np.min(final))

cv2.imshow("final", final)

cv2.imwrite("floor_dist/floor_dist.jpg", final)

cv2.waitKey(0)