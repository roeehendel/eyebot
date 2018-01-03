import cv2
import numpy as np

import margins.line_helper as LineHelper
from margins.filter_by_color import filter_image_by_color
from margins.line_array import LineArray


class LineIdentifier:
    def __init__(self, img):
        self.H = len(img)
        self.W = len(img[0])
        self.minLineLength = int(self.H / 13)
        self.maxLineGap = int(self.H / 15)
        self.threshold = int(self.W / 100)  # threshold for houghlines
        self.vertices = np.array(
            [[0, self.H * 1 / 3], [self.W, self.H * 1 / 3],
             [self.W, self.H], [0, self.H]])  # lower half

        self.right_lines_array = LineArray(self.W / 20)
        self.left_lines_array = LineArray(self.W / 20)

    def roi(self, img, vertices):  # taking only the region of interest
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, np.int32([vertices]), 255)
        masked = cv2.bitwise_and(img, mask)
        return masked

    def find_lines(self, original_img):
        mask = filter_image_by_color(original_img)
        processed = self.roi(mask, [self.vertices])
        lines = cv2.HoughLinesP(processed, 1, np.pi / 100,
                                threshold=self.threshold,
                                minLineLength=self.minLineLength,
                                maxLineGap=self.maxLineGap)

        if lines is None:  # dealing with the None case
            lines = []

        return processed, lines

    def get_margins_from_image(self, im):
        _, lines = self.find_lines(im)
        left, right = self.get_left_and_right(lines)
        return (left, right)

    def get_left_and_right(self, lines):

        lefts, rights = [], []
        for line in lines:
            r, theta = LineHelper.get_r_and_theta(line)

            if theta > 0:
                rights.append(line)
            elif theta < 0:
                lefts.append(line)

        left = self.left_lines_array.get_line_from_cluster(lefts)
        right = self.right_lines_array.get_line_from_cluster(rights)

        if left is not None:
            left = self.left_lines_array.filter_line(left)
        if right is not None:
            right = self.right_lines_array.filter_line(right)

        #todo check WTF?
        return right, left
