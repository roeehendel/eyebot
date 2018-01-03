import numpy as np

class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.lx = x1
        self.ly = y1
        self.rx = x2
        self.ry = y2
        self.is_real = False

    def distance(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def direction(self):
        if self.x >= 0:
            return np.arctan(self.y / self.x)
        if self.x < 0:
            return np.arctan(self.y / self.x) + np.pi

    def __str__(self):
        return '[({:1.1f},{:1.1f}),({:1.1f},{:1.1f})]'\
            .format(self.lx, self.ly, self.rx, self.ry)
