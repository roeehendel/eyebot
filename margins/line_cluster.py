import numpy as np

import margins.line_helper as line_helper


class Cluster:
    def __init__(self, line, max_radius_distance, max_theta_distance):
        self.low_point, self.high_point = line_helper.get_low_point_and_high_point(line)

        self.ymin = self.low_point[1]
        self.ymax = self.high_point[1]

        r0, theta0 = line_helper.get_r_and_theta(line)

        a, b = line_helper.get_A_and_B(line)

        # sign of the line's intersection with the y axis.
        self.sign = np.sign(b)

        self.max_radius_distance = max_radius_distance
        self.max_theta_distance = max_theta_distance

        # arrays for the lines radii and thetas
        self.thetas = [theta0]
        self.radii = [r0]

        self.mean_radius = np.mean(self.radii)
        self.mean_theta = np.mean(self.thetas)

    def line_is_close(self,line, r, theta):
        """
        checking wether or not a line belongs in the cluster.
        if yes, it also adds it to the cluster.
        :param r: line's r
        :param theta: line's angle
        :return: true if line belongs, false otherwise.
        """

        is_close = (abs(r - self.mean_radius) < self.max_radius_distance and
                    abs(theta - self.mean_theta) < self.max_theta_distance)

        if is_close:
            self.add(line)

        return is_close

    def update_means(self):
        self.mean_radius = np.mean(self.radii)
        self.mean_theta = np.mean(self.thetas)

    def add(self, line):
        """adding a line to the cluster, given by r and theta"""

        r, theta = line_helper.get_r_and_theta(line)
        low, high = line_helper.get_low_point_and_high_point(line)

        if low[1] < self.ymin:
            self.ymin = low[1]
            self.low_point = low
        if high[1] > self.ymax:
            self.ymin = high[1]
            self.high_point = high

        self.radii.append(r)
        self.thetas.append(theta)

        self.update_means()

    def return_line(self):
        return [[self.low_point[0], self.low_point[1],self.high_point[0],self.high_point[1]]]

    def __len__(self):
        return len(self.radii)
