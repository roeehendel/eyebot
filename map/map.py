import numpy as np
import copy


class Map:
    """
    @:param left_line  - a tuple (a,b,c) that represent the line ax+by+c=0
    @:param right_line - a tuple (a,b) that represent the line ax+by+c=0
    @:param obs - a list of obstacles(obstacle type)
    @:param width - the width of the road

    """

    def __init__(self, left_line, right_line, obs, width):
        self.aligned_left_line = None
        self.aligned_right_line = None
        self.left_line = left_line  # the left border of the sidewalk
        self.right_line = right_line  # the right border of the sidewalk
        self.obs = obs  # a list of obstacle type
        self.original_obs = obs  # a list of obstacle type
        self.width = width
        self.my_x = self.distance_from_line(0, 0, left_line)
        self.my_y = 0
        self.align()  # rotate the coordinates to be parallel

    def my_angle(self):
        if self.left_line[1] == 0:
            return 0
        ratio = np.abs(self.left_line[0] / self.left_line[1])
        cos_theta = ratio / np.sqrt(ratio ** 2 + 1)
        theta = np.arccos(cos_theta)*(180/np.pi)
        return theta*np.sign(-1*self.left_line[0]/self.left_line[1])

    def distance_from_line(self, x, y, line):
        """
        calculate the distance of (x,y) from the a line.
        :param x: x coordinate
        :param y: y coordinate
        :param line: a tuple (a,b,c) that represent ax+by+c = 0
        :return: distance of (x,y) from the line "line"
        """
        mone = np.abs(line[0] * x + line[1] * y + line[2])
        mech = np.sqrt(line[0] ** 2 + line[1] ** 2)
        return mone / mech

    def distance_in_lane(self, y):
        """
        calculate the distance of an obstacle inside the lane
        :param y: the obstacle y coordinate
        :return:  distance of the obs inside the lane
        """
        if self.left_line[1] == 0:
            return y
        ratio = np.abs(self.left_line[0] / self.left_line[1])
        sin_theta = ratio / np.sqrt(ratio ** 2 + 1)
        return y / sin_theta

    def align_obstacles(self, obstacles):
        for ob in obstacles:
            # rotating left coordinate
            future_lx = self.distance_from_line(ob.lx, ob.ly, self.left_line)
            future_ly = self.distance_in_lane(ob.ly)
            if self.distance_from_line(ob.lx, ob.ly, self.right_line) > self.width:
                future_lx = 0
            ob.lx = future_lx
            ob.ly = future_ly
            # rotating right coordinate
            future_rx = self.distance_from_line(ob.rx, ob.ry, self.left_line)
            future_ry = self.distance_in_lane(ob.ry)
            if self.distance_from_line(ob.rx, ob.ry, self.right_line) > self.width:
                future_rx = self.width
            ob.rx = future_rx
            ob.ry = future_ry

    def check_if_obstacles_are_in_lane(self, obstacles):
        # Delete obstacles that are not in the sidewalk
        for ob in obstacles:
            l_dis = self.distance_from_line(ob.rx, ob.ry, self.right_line)
            r_dis = self.distance_from_line(ob.rx, ob.ry, self.right_line)

            if self.distance_from_line(ob.rx, ob.ry, self.right_line) < self.width:
                if self.distance_from_line(ob.lx, ob.ly, self.left_line) < self.width:
                    ob.is_real = True

    def align(self):

        self.aligned_left_line = (1, 0, 0)
        self.aligned_right_line = (1, 0, -self.width)
        new_obs = []

        self.check_if_obstacles_are_in_lane(self.obs)

        self.original_obs = copy.deepcopy(self.obs)

        self.obs = [obs for obs in self.obs if obs.is_real]

        self.align_obstacles(self.obs)
        self.align_obstacles(self.original_obs)

        # Align obstacles

        self.my_x = self.distance_from_line(0, 0, self.left_line)
        self.my_y = 0
