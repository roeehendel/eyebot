import cv2
import numpy as np

def filter_contours_by_size(contours,minArea):
    filtered_contours = []
    for cnt in contours:
        if cv2.contourArea(cnt)>minArea:
            filtered_contours.append(cnt)

    return filtered_contours

def get_convex_hulls(contours):
    hulls = []
    for cnt in contours:
        hulls.append(cv2.convexHull(cnt))
    return hulls