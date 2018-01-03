import logging

logging.basicConfig(level=logging.INFO)

import cv2
import numpy as np
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
from pyrealsense import rsutilwrapper


class CameraControl:
    def __init__(self):
        self.floor_depth = cv2.imread("floor_dist/floor_approx.jpg", cv2.IMREAD_GRAYSCALE)

        self.floor_depth = self.floor_depth.astype(np.float16)

        self.floor_depth = self.floor_depth * (4.0 / 255.0)

        self.serv = pyrs.Service()
        self.dev = self.serv.Device(streams=[pyrs.stream.DepthStream(width=640, height=480),
                                             pyrs.stream.ColorStream(width=640, height=480)])
        self.extrinsics = self.dev.get_device_extrinsics(self.dev.streams[1].stream, self.dev.streams[0].stream)

        self.dev.apply_ivcam_preset(8)


        try:  # set custom gain/exposure values to obtain good depth image
            custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 1000.0),
                              (rs_option.RS_OPTION_R200_LR_GAIN, 200.0),
                              (rs_option.RS_OPTION_R200_DEPTH_CONTROL_ESTIMATE_MEDIAN_DECREMENT, 3),
                              (rs_option.RS_OPTION_R200_DEPTH_CONTROL_ESTIMATE_MEDIAN_INCREMENT, 23),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_MEDIAN_THRESHOLD, 0),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_SCORE_MINIMUM_THRESHOLD, 9),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_SCORE_MAXIMUM_THRESHOLD, 1023),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_TEXTURE_COUNT_THRESHOLD, 0),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_TEXTURE_DIFFERENCE_THRESHOLD, 0),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_SECOND_PEAK_THRESHOLD, 0),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_NEIGHBOR_THRESHOLD, 0),
                              # (rs_option.RS_OPTION_R200_DEPTH_CONTROL_LR_THRESHOLD, 2048)
                              ]
            self.dev.set_device_options(*zip(*custom_options))
        except pyrs.RealsenseError:
            pass  # options are not available on all devices

    def depth_scale(self):
        return self.dev.depth_scale

    def get_frames(self):
        self.dev.wait_for_frames()

        self.color_img = self.dev.color
        self.depth_img = self.dev.depth

        return self.color_img, self.depth_img

    def floor_world_position(self, pixel):
        return self.pixel_world_position(pixel, self.floor_depth)

    def pixel_world_position_by_depth(self, pixel, depth):
        depth_pixel = np.array(pixel).astype(np.float32)

        depth_point = self.dev.deproject_pixel_to_point(depth_pixel, depth)

        return depth_point

    def pixel_world_position(self, pixel, depth_img=None):
        if depth_img is None:
            depth_img = self.depth_img * self.depth_scale()

        depth_in_meters = depth_img[np.math.floor(pixel[1]), np.math.floor(pixel[0])]

        return self.pixel_world_position_by_depth(pixel, depth_in_meters)

    def close(self):
        self.serv.close()
        self.dev.close()
