import math

import cv2
import numpy as np


class InitialObstacle:
    obstacles = []
    min_distance_dif = 0.7

    def __init__(self, contour, x_left, x_right, y, D, min_distance):
        """

        :param contour: contours surrounding the object
        :param D: "average distance" (obstacle's distance)
        :param min_distance: minimal distance between 2 obstacle centers needed
                             to distinguish them different.
        """
        self.contour = contour
        self.x_left = x_left
        self.x_right = x_right

        # the center coordinates
        self.Y = y
        self.X = int((x_left + x_right) / 2)
        self.D = D
        self.min_distance = min_distance

    @staticmethod
    def get_left_and_right(contour):
        """
        returning middle left and middle right points of contour.
        :param contour:
        :return:
        """
        x, y, w, h = cv2.boundingRect(contour)

        x_left, x_right = x, x + w
        y_middle = int(y + h / 2)

        return [x_left, y], [x_right, y]

    @staticmethod
    def add_obstacle(obstacle):
        x1 = int((obstacle.x_left + obstacle.x_right) / 2)
        y1 = obstacle.Y

        for obst in InitialObstacle.obstacles:
            x2 = int(obst.x_left + obst.x_right)
            y2 = obst.Y

            if (abs(obst.D - obstacle.D) < InitialObstacle.min_distance_dif and
                        math.hypot(obst.X - obstacle.X,
                                   obst.Y - obstacle.Y) < obstacle.min_distance):
                # merging the two close contours together
                InitialObstacle.obstacles.remove(obst)
                obstacle = InitialObstacle(
                    cv2.convexHull(
                        np.vstack([obstacle.contour, obst.contour])),
                    # connected contour
                    min(obst.x_left, obstacle.x_left),
                    max(obst.x_right, obstacle.x_right),
                    int((obst.Y + obstacle.Y) / 2),
                    min(obstacle.D, obst.D),
                    obstacle.min_distance
                )
                break
        InitialObstacle.obstacles.append(obstacle)

    @staticmethod
    def reset_obstacles():
        InitialObstacle.obstacles = []

    def get_list_representation(self):
        return [self.x_left, self.x_right, self.Y, self.D]
