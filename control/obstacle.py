import numpy as np


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def direction(self):
        if self.x >= 0:
            return np.arctan(self.y / self.x)
        if self.x < 0:
            return np.arctan(self.y / self.x) + np.pi
