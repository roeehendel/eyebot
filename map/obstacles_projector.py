from map.obstacle import Obstacle


class ObstaclesProjector:
    def __init__(self, camera):
        self.camera = camera
        self.obstacles = []

    def update_obstacles(self, images_obstacles):
        self.obstacles = []
        for images_obstacle in images_obstacles:
            self.obstacles.append(self.project_obstacle_to_world(images_obstacle))

    def project_obstacle_to_world(self, obstacle):
        left_point = self.camera \
            .pixel_world_position_by_depth \
            ([obstacle[0], obstacle[2]], obstacle[3])
        right_point = self.camera \
            .pixel_world_position_by_depth \
            ([obstacle[1], obstacle[2]], obstacle[3])

        return Obstacle(left_point[0], left_point[2],
                        right_point[0], right_point[2])
