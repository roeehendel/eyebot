import os
import cv2
import numpy as np

DIR = "floor_dist/floor_benny/depth/"

final = cv2.imread(DIR + "d0.jpg", cv2.IMREAD_GRAYSCALE)

list_of_pictures = []

for filename in os.listdir(DIR):
    img = cv2.imread(DIR + filename,  cv2.IMREAD_GRAYSCALE)
    list_of_pictures.append(img)
arr3d = np.array(list_of_pictures)
for i in range(0, len(list_of_pictures[0])):
    print(i)
    for j in range(0, len(list_of_pictures[0][0])):
        relevant_pixels = []
        for k in range(0, len(list_of_pictures)):
            if list_of_pictures[k][i][j] != 0:
                relevant_pixels.append(list_of_pictures[k][i][j])
        if relevant_pixels == []:
            final[i][j] = 255
        else:
            final[i][j] = np.median(relevant_pixels)


cv2.imwrite("floor_dist/floor_dist_benny.jpg", final)

cv2.waitKey(0)