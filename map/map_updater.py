from map.lanes_projector import LanesProjector
from map.obstacles_projector import ObstaclesProjector


class MapUpdater:
    def __init__(self, map, camera):
        self.map = map
        self.lanes_projector = LanesProjector(camera)
        self.obstacle_projector = ObstaclesProjector(camera)

    def update_lanes(self, left_image_lane, right_image_lane):
        self.lanes_projector.update_lanes(left_image_lane, right_image_lane)
        if self.lanes_projector.left_world_lane is not None:
            self.map.left_line = self.lanes_projector.left_world_lane
        if self.lanes_projector.right_world_lane is not None:
            self.map.right_line = self.lanes_projector.right_world_lane

    def update_obstacles(self, image_obstacles):
        self.obstacle_projector.update_obstacles(image_obstacles)
        self.map.obs = self.obstacle_projector.obstacles
