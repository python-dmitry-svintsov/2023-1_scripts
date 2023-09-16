import pygame as pg
import numpy as np
import math


class VoxelRender2:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = math.pi / 6
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2000
        self.scale_height = 920
        self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))
        # self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))
        #
        self.height_map_img = pg.image.load('.\\venv\\apps\\voksel3d\\texture_map\\height_map.jpg')
        self.height_map = pg.surfarray.array3d(self.height_map_img)

        self.color_map_img = pg.image.load('.\\venv\\apps\\voksel3d\\texture_map\\color_map.jpg')
        self.color_map = pg.surfarray.array3d(self.color_map_img)

        self.map_height = len(self.height_map[0])
        self.map_width = len(self.height_map)

    def ray_casting(self):
        self.screen_array = np.random.randint(0, 255, size=self.screen_array.shape)

    def update(self):
        self.ray_casting()

    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))