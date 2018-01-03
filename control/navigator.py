import numpy as np

import control.PID as PID


class Navigator:
    # environment parameters
    LANE_NUM = 8
    MINIMUM_DISTANCE = 3.5  # minimum distance for a lane to be "empty"
    BIG_BIG_NUMBER = 1000  # a number that is big enough for our system
    # PID constants
    PROPORTIONAL = 1  # P const
    INTEGRAL = 0  # I const
    # integral is limite
    DERIVATIVE = 1.25  # D const
    # try (1.5, 0.0007, 0.0006)
    # other related PID constants
    DERIVATOR = 0
    INTEGRATOR = 0
    INTEGRATOR_MAX = 500  # high bound for the integrator
    INTEGRATOR_MIN = -500  # lower bound for the integrator
    # constants  related to moving the car
    DESIRABLE_STEERING = 1  # bound for the steering amount we want

    UPDATE_LEFT_DIST_EVERY = 1

    def __init__(self, my_map, lanes=LANE_NUM):
        """
        @:param my_ma[ - map object of the world
        @:param lanes - the number of lanes - logic number
        """
        self.lane_num = lanes
        self.map = my_map
        self.lanes = self.lane_map()
        self.pid = PID.PID(self.PROPORTIONAL, self.INTEGRAL, self.DERIVATIVE,
                           self.DERIVATOR, self.INTEGRATOR,
                           self.INTEGRATOR_MAX, self.INTEGRATOR_MIN)

        self.left_dist_history = []
        self.left_dist = 0

        self.steer_value = 0

        # self.pid = PID.PID(self.PROPORTIONAL, self.INTEGRAL, self.DERIVATIVE)
        # self.pid.setSampleTime(0.2)

    def update(self):
        """
        this function is activated every time the map is updating.
        creates up to date lane map
        :return:
        """
        self.lanes = self.lane_map()
        current_left_dist = self.map.my_x
        self.left_dist_history.append(current_left_dist)
        if len(self.left_dist_history) > self.UPDATE_LEFT_DIST_EVERY:
            self.left_dist = np.average(self.left_dist_history)
            self.left_dist_history = []
            return True
        return False

    def get_lane(self, x):
        """
        calculates the lane of a point (x,y) in the world
        :param x: x coordinate
        :return: the lane number (a number between 0 to (lane_num -1 )
        """
        # print("line", self.map.left_line)
        # print("dist from left line", self.dist_from_line(self.map.left_line, x, y))
        return int(np.floor((x / self.map.width) * self.lane_num))

    def lane_map(self):
        """
        generate a map of the lanes, and the obstacles in every lane. every lane is
        sorted from the nearest obstacle to the farest obstalce
        :param self:
        :return: a sorted list of lists with size of lane_num. every sub list is the
        representation of the #i's lane
        """
        lanes = []
        for i in range(self.lane_num):
            lanes.append([])
        for obstacle in self.map.obs:
            left_lane = max(self.get_lane(obstacle.lx), 0)
            left_depth = obstacle.ly
            right_lane = min(self.get_lane(obstacle.rx), self.lane_num - 1)
            right_depth = obstacle.ry
            for j in range(right_lane - left_lane + 1):
                depth_delta = right_depth - left_depth
                depth_interval = depth_delta / (right_lane - left_lane)
                lanes[left_lane + j].append(left_depth + (depth_interval * j))
        for lane in lanes:
            lane.sort()
        return lanes

    def choose_lane(self):
        # # Todo: remove to enable actual lane choice
        # return 7
        lanes_weight = []  # this list contains in the i'th place the distance
        # of the nearest object in the i'th lane
        for i in range(len(self.lanes)):
            if len(self.lanes[i]) == 0:  # if no obstacles in this lane
                lanes_weight.append(
                    self.BIG_BIG_NUMBER)  # -1 means this lane is empty
            else:  # add the distance of the nearest obstacle to be the value
                lanes_weight.append(self.lanes[i][0])
        if min(lanes_weight) == self.BIG_BIG_NUMBER:
            return int(np.round(self.lane_num / 2))
        my_lane = self.get_lane(self.map.my_x)
        to_conv = [1, 3, 9, 3, 1]
        new_weight = np.convolve(lanes_weight, to_conv)
        chosen = np.argmax(new_weight) - 2
        chosen = max(chosen, 1)
        chosen = min(chosen, self.lane_num - 2)
        return chosen

        # check if the chosen lane should be the middle
        """ old code"""
        # mid_lane = int(np.round(self.lane_num / 2))
        # if (mid_lane >= my_lane):
        #     middle_lanes = list(range(my_lane, mid_lane + 1))
        # else:
        #     middle_lanes = list(range(my_lane, mid_lane - 1, -1))
        # go_mid = True
        # diff = self.MINIMUM_DISTANCE / len(middle_lanes)
        # for j in range(len(middle_lanes)):
        #     if lanes_weight[middle_lanes[j]] < diff * (j + 1):
        #         go_mid = False
        #         break
        # if go_mid:
        #     return mid_lane
        # # check if should stay in the current lane
        # if lanes_weight[my_lane] > self.MINIMUM_DISTANCE:
        #     return my_lane
        # # a change in lane is needed. check for the (lane_num)/3 lanes around
        # # the current location
        # area = int(max(np.round(self.lane_num / 6), 1))
        # potential_near = list(range(my_lane - area, my_lane + area + 1))
        # near_lanes = []
        # for num in potential_near:
        #     if num in range(0, self.lane_num):
        #         near_lanes.append(num)
        # # potential near contains the existing nearest lanes to my_lane
        # chosen = near_lanes[0]
        # for lane in near_lanes:
        #     if lanes_weight[lane] > lanes_weight[chosen]:
        #         chosen = lane
        # return chosen

    def steer(self):
        """
        determines the steering angle for the next movement
        :return: the steering angle
        """
        updated = self.update()  # update the lane map with the new information
        # in the map
        if updated:
            goal_lane = self.choose_lane()
            print(goal_lane)
            goal_left_dist = goal_lane / self.lane_num * \
                             self.map.width

            error = self.left_dist - goal_left_dist

            self.steer_value = self.pid.update(error, -np.sin((np.pi / 180) *
                                                              self.map.my_angle()))  # a number that is proportional to the fix in steering
            # normalize the steering to the desirable values
            if self.steer_value > self.DESIRABLE_STEERING:
                self.steer_value = self.DESIRABLE_STEERING
            elif self.steer_value < -1 * self.DESIRABLE_STEERING:
                self.steer_value = -1 * self.DESIRABLE_STEERING

        return self.steer_value
