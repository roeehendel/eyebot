import cv2
import numpy as np
import time

import obstacles.contour_sorter as cs
from obstacles.initial_obstacle import InitialObstacle


class ObstacleIdentifier:
    def __init__(self, img):
        self.SCALE = 4

        self.H = int(len(img) / self.SCALE)
        self.W = int(len(img[0]) / self.SCALE)

        # min and max values of grayscale
        self.minval = 30
        self.maxval = 100
        self.numOfLayers = 1  # number of seperated obstacle layers

        self.thersholdStep = int(
            (self.maxval - self.minval) / self.numOfLayers)

        self.minArea = int((self.H * self.W) / 50)
        self.contours = []  # list of contours

        # upper half
        # todo fix boundaries: maybe not 2 thirds?
        self.vertices = np.array(
            [[0, self.H * 1 / 3],
             [self.W, self.H * 1 / 3],
             [self.W, self.H * 3 / 4],
             [0, self.H * 3 / 4]])

        # factor between greyscale to distance
        self.distance_factor = float(4) / float(255)

    def roi(self, img):  # taking only the region of interest
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, np.int32([self.vertices]), 255)
        masked = cv2.bitwise_and(img, mask)
        return masked

    def identify_obstacles(self, d):
        """
        identifying obstacles in a depth image. InitialObstacle
        :param depth:
        :return:
        """

        # threshold
        ret, depth = cv2.threshold(d, 0.6, 4, cv2.THRESH_TOZERO)

        depth = depth * (1.0 / 4.0)

        depth = depth * 255

        depth = depth.astype(np.uint8)

        depth = cv2.resize(depth, (self.W, self.H))

        # cutting the image
        depth = self.roi(depth)

        InitialObstacle.reset_obstacles()

        for i in range(self.numOfLayers):
            # this layer thresholds
            minval = self.minval + i * self.thersholdStep
            maxval = minval + self.thersholdStep

            self.identify_obstacles_in_layer(depth, minval, maxval)

        """update current object's contour list and return obstacles in wanted
        representation"""

        self.contours = [obst.contour for obst in InitialObstacle.obstacles]

        obstacles = [obst.get_list_representation() for obst in
                     InitialObstacle.obstacles]

        return obstacles

    def identify_obstacles_in_layer(self, depth, minval, maxval):

        """
        getting the obstacles in a specific depth layer
        :param depth: depth image
        :param minval: min value of layer
        :param maxval: max value of layer
        :return: list of current obstacles found in layer.
        """

        mask = cv2.inRange(depth, minval, maxval)
        depth = depth.astype(np.uint8)
        masked = cv2.bitwise_and(depth, mask)

        # blurring the image
        blurred = cv2.medianBlur(masked, 9)
        blurred = cv2.medianBlur(blurred, 9)

        # kernel = np.ones((40, 40), np.uint8)
        # blurred = cv2.dilate(blurred, kernel)

        im2, cur_contours, hierarchy = cv2.findContours(blurred,
                                                        cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_SIMPLE)

        cur_contours = cs.filter_contours_by_size(cur_contours,
                                                  self.minArea)

        # adding the new obstacles to our obstacle list.
        for cnt in cur_contours:
            self.create_initial_obstacle_from_contour(cnt, masked)

    def create_initial_obstacle_from_contour(self, contour, img):
        x, y, w, h = cv2.boundingRect(contour)

        # midpoints
        x_left, x_right = x, x + w
        y_middle = int(y + h / 2)

        # calculating the average distance
        # todo no magic number 2
        count = 1
        sum = 0
        for i in range(x, x + w, 2):  # skipping 10 each time: runtime.
            for j in range(y, y + h, 2):
                val = img[j, i]  # it's y,x for some reason.
                if val > 4:
                    count += 1
                    sum += val

        average_gray = sum / count
        D = average_gray * self.distance_factor  # average distance

        # todo remove magic number 20
        obstacle = InitialObstacle(contour,
                                   x_left * self.SCALE,
                                   x_right * self.SCALE,
                                   y_middle * self.SCALE, D,
                                   min_distance=200)
        InitialObstacle.add_obstacle(obstacle)
