#
# External libraries
#

import cv2

#
# Local libraries
#

# Controllers
import numpy as np
import time

from controllers.depth_camera_control import CameraControl
from controllers.vehicle_control import VehicleControl
from controllers.force_control import ForceClass

# Detection
from margins.line_identifier import LineIdentifier
import margins.display_helper as display_helper
from obstacles.find_obstacles_main import ObstacleIdentifier

# Map
from map.map import Map
from map.map_updater import MapUpdater

# Control
from control.navigator import Navigator

from matplotlib import pyplot as plt

VEHICLE_PORT = "/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00"
FORCE_PORT = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"
STOP = 100

#
# Initialization
#

init_steps = 10
steps = 0

# Init controllers
vehicle_control = VehicleControl(VEHICLE_PORT)
camera = CameraControl()
force_control = ForceClass(FORCE_PORT)
# time.sleep(5)

# Init map and updater
main_map = Map((0, 0, 0), (0, 0, 0), [], 1.33)
map_updater = MapUpdater(main_map, camera)

# Init navigator
navigator = Navigator(main_map)

# Init margin detection
c, d = camera.get_frames()
line_identifier = LineIdentifier(c)
obstacle_identifier = ObstacleIdentifier(d)


def step():
    global init_steps, steps

    c, d = camera.get_frames()

    c = cv2.cvtColor(c, cv2.COLOR_BGR2RGB)

    display_image = c.copy()

    # detect lanes in image
    right_image_lane, left_image_lane = line_identifier.get_margins_from_image(c)

    # detect obstacles
    obstacles = obstacle_identifier.identify_obstacles(d * camera.depth_scale())

    # d_obs = cv2.resize(d_obs, (obstacle_identifier.W, obstacle_identifier.H))

    # display_helper.draw_obstacles(d_obs,
    #                               obstacle_identifier.contours)

    # cv2.imshow('dobs', d_obs)

    # update map to include detected lines
    map_updater.update_lanes(left_image_lane, right_image_lane)

    # update map to include detected obstacles
    map_updater.update_obstacles(obstacles)

    # for o in main_map.obs:
    #     print(o)

    # stop if the user stopped
    # if force_control.read_details() > STOP:
    #     vehicle_control.reset()
    #     while force_control.read_details() > STOP:
    #         continue

    # get control values
    if steps > init_steps:
        main_map.align()

        # display image with detected lanes
        display_helper.draw_lines(display_image, [left_image_lane, right_image_lane])

        steer_value = navigator.steer()

        vehicle_control.drive_after_pid(steer_value)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(display_image,
                    'l_d: {:2.2f}, s_v: {:2.2f}, d_v: {:2.2f}, th: {:2.2f}'
                    .format(main_map.my_x,
                            steer_value,
                            navigator.pid.D_value,
                            main_map.my_angle()),
                    (10, 30), font, 0.8,
                    (0, 0, 255), 2,
                    cv2.LINE_AA)

        # display_helper.draw_obstacles(display_image,
        #                               obstacle_identifier.contours)

        display_helper.draw_obstacles_points(display_image, obstacles, main_map.original_obs)

        cv2.imshow("GUI", display_image)
        cv2.waitKey(1)

    # control the vehicle

    steps += 1


while True:
    try:
        step()
    except Exception:
        print("Exception")
    # step()
