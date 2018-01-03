import numpy as np

from margins import line_helper
from matplotlib import pyplot as plt


class LanesProjector:
    def __init__(self, camera):
        self.left_image_lane = None
        self.right_image_lane = None
        self.left_world_lane = None
        self.right_world_lane = None
        self.distance = 1.33
        self.camera = camera

        self.x_min = 0
        self.x_max = 640 - 1 - 0
        self.y_min = 310
        self.y_max = 480 - 1

    def update_lanes(self, left_image_lane, right_image_lane):
        self.left_world_lane = None
        self.right_world_lane = None
        if left_image_lane is not None:
            self.left_image_lane = left_image_lane
            self.left_world_lane = self.project_lane_to_world(left_image_lane)
        if right_image_lane is not None:
            self.right_image_lane = right_image_lane
            self.right_world_lane = self.project_lane_to_world(right_image_lane)

        if right_image_lane is not None and left_image_lane is not None \
                and self.right_world_lane is not None and self.left_world_lane is not None:
            self.make_lanes_parallel()
            # self.distance = np.abs(self.right_world_lane[1] - self.left_world_lane[1]) /\
            #                 np.sqrt(self.left_world_lane[0] ** 2 + 1)
        elif right_image_lane is not None and self.right_world_lane is not None:
            # b_diff = self.distance / np.cos(np.arctan(self.right_world_lane[0]))
            b_diff = self.distance * np.sqrt(self.right_world_lane[1] ** 2 + 1)
            self.left_world_lane = [-1, self.right_world_lane[1], self.right_world_lane[2] - b_diff]
        elif left_image_lane is not None and self.left_world_lane is not None:
            # b_diff = self.distance / np.cos(np.arctan(self.left_world_lane[0]))
            b_diff = self.distance * np.sqrt(self.left_world_lane[1] ** 2 + 1)
            self.right_world_lane = [-1, self.left_world_lane[1], self.left_world_lane[2] - b_diff]

    def has_both_lanes(self):
        return self.left_world_lane is not None and self.right_world_lane is not None

    def get_world_lanes(self):
        return self.left_world_lane, self.right_world_lane

    def project_lane_to_world(self, lane):

        a, b = line_helper.get_A_and_B(lane)

        lane = line_helper.part_blocked_in_rect(a, b,
                                                self.x_min,
                                                self.y_min,
                                                self.x_max,
                                                self.y_max)

        points_2d = line_helper.points_on_line(lane)

        points_3d = np.apply_along_axis(self.camera.floor_world_position, 0, points_2d)

        # condition = points_3d[2] > 0.2
        condition = (1.4 < points_3d[2]) & (points_3d[2] < 3.5)

        points_3d_filtered = np.transpose(np.transpose(points_3d)[condition])

        # condition_2 = points_3d_filtered[0] < -1.5

        # points_3d_filtered = np.transpose(np.transpose(points_3d_filtered)[condition_2])

        if points_3d_filtered.size > 5:
            lane_3d = np.polyfit(-points_3d_filtered[2], points_3d_filtered[0], 1)

            f = np.poly1d(lane_3d)

            # calculate new x's and y's
            x_new = np.linspace(-2, 2, 100)
            y_new = f(x_new)

            # plt.plot(-points_3d_filtered[2], points_3d_filtered[0],  "o")
            # plt.plot(x_new, y_new,  ".")
            # plt.axis([-4, 0, -2, 2])
            # plt.show()

            lane_3d = [-1, -lane_3d[0], lane_3d[1]]

            return lane_3d

        return None

    def make_lanes_parallel(self):
        a1 = self.right_world_lane[1]
        a2 = self.left_world_lane[1]
        a = np.mean([a1, a2])
        self.right_world_lane[1] = a
        self.left_world_lane[1] = a
