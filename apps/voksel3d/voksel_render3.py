
import pygame as pg
from numba import njit
import numpy as np
import math
import taichi as ti


@ti.data_oriented
class VoxelRender3:
    def __init__(self, app):
        self.app = app
        self.player = self.app.player
        self.fov = math.pi / 6
        self.h_fov = self.fov / 2
        self.num_rays = self.app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 1200
        self.scale_height = 920
        # taichi
        ti.init(arch=ti.cpu)
        # self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))
        self.height_map_img = pg.image.load('.\\venv\\apps\\voksel3d\\texture_map\\height_map.jpg')
        self.h_map = pg.surfarray.array3d(self.height_map_img)
        self.color_map_img = pg.image.load('.\\venv\\apps\\voksel3d\\texture_map\\color_map.jpg')
        self.c_map = pg.surfarray.array3d(self.color_map_img)
        self.map_width, self.map_height = self.height_map_img.get_size()
        #
        self.height_map = ti.Vector.field(3, ti.int16, (self.map_width, self.map_height))
        self.color_map = ti.Vector.field(3, ti.int16, (self.map_width, self.map_height))
        self.height_map.from_numpy(self.h_map)
        self.color_map.from_numpy(self.c_map)
        self.screen_array = np.full((self.app.width, self.app.height, 3), [0, 0, 0], dtype=np.uint16)
        self.screen_field = ti.Vector.field(3, ti.int16, (self.app.width, self.app.height))
        #
        self.y_buffer = ti.field(ti.int32, self.app.width)

    @ti.kernel
    def ray_casting(self):
        for num_ray in ti.ndrange(self.app.width):
            ray_angle = self.player.angle - self.h_fov + self.delta_angle * num_ray
            first_contact = False
            sin_a = ti.sin(ray_angle)
            cos_a = ti.cos(ray_angle)

            for depth in range(1, self.ray_distance):
                x = int((self.player.pos[0] + depth * cos_a))
                if 0 < x < self.map_width:
                    y = int((self.player.pos[1] + depth * sin_a))
                    if 0 < y < self.map_height:

                        # remove fish eye and get height on screen
                        # depth *= ti.cos(self.player.angle - ray_angle)
                        f = depth * ti.cos(self.player.angle - ray_angle)
                        height_on_screen = int((self.player.height - self.height_map[x, y][0]) /
                                               f * self.scale_height + self.player.pitch)
                        height_on_screen = ti.min(ti.max(height_on_screen, 0), self.app.height)

                        # remove unnecessary drawing
                        if not first_contact:
                            self.y_buffer[num_ray] = height_on_screen
                            first_contact = True

                        # draw vert line
                        if height_on_screen < self.y_buffer[num_ray]:
                            for screen_y in range(height_on_screen, self.y_buffer[num_ray]):
                                self.screen_field[num_ray, screen_y] = self.color_map[x, y]
                            self.y_buffer[num_ray] = height_on_screen

    @ti.kernel
    def buffer_reset(self):
        for x in self.y_buffer:
            self.y_buffer[x] = 0

    @ti.kernel
    def reset_screen_field(self):
        for x, y in self.screen_field:
            self.screen_field[x, y] = (0, 0, 0)

    def update(self):
        self.reset_screen_field()
        self.buffer_reset()
        self.ray_casting()
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

