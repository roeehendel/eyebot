import math
import time
import numpy as np

from margins.line_cluster import Cluster
from margins.line_helper import get_r_and_theta


class LineArray:
    def __init__(self, max_radius_distance):
        self.max_size = 10

        # arrays for the lines radii and thetas
        self.thetas = []
        self.radii = []

        # distances by which given lines will be filtered, according to current averages
        self.max_radius_distance = max_radius_distance
        self.max_theta_distance = math.pi / 8

    def filter_line(self, line):
        r, theta = get_r_and_theta(line)

        # updating arrays
        self.radii.insert(0, r)
        self.thetas.insert(0, theta)

        mean_radius = np.mean(self.radii)
        mean_theta = np.mean(self.thetas)

        # if too  long - kicking out last object added. (FIFO)
        if len(self.radii) > self.max_size:
            self.radii.pop()
            self.thetas.pop()

        # filtering the line: returning if sufficiently close to average
        if abs(r - mean_radius) < self.max_radius_distance and \
                        abs(theta - mean_theta) < self.max_theta_distance:
            return line

        # if not.. return the None line.
        return None

    def get_line_from_cluster(self, lines):
        """
        returning r,theta of
        :param lines:
        :return: r, theta of max cluster.
        """
        if len(lines) == 0:
            return None
        clusters = []
        for line in lines:
            r, theta = get_r_and_theta(line)
            added = False
            for cluster in clusters:
                if cluster.line_is_close(line, r, theta):
                    added = True
                    break

            # if no matching cluster was found, create a new one.
            if not added:
                clusters.append(Cluster(line, self.max_radius_distance,
                                        self.max_theta_distance))
        # returning the r,theta of our line
        max_cluster = max(clusters, key=len)

        return max_cluster.return_line()

        # now, finding the largest cluster
