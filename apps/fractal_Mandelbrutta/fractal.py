import pygame as pg
import numpy as np


class Fractal_1:
    def __init__(self, main):
        self.main = main
        self.screen, self.screen_width, self.screen_height, self.delta_dite = self.main.get_basik_values()
        self.screen_array = np.full((self.screen_width, self.screen_height, 3), [0, 0, 0], dtype=np.uint8)
        #
        self.get_texture()
        #
        self.offset = np.array([1.3 * self.screen_width, self.screen_height]) // 2
        self.max_iter = 30
        self.zoom = 2.2 / self.screen_height

    def get_texture(self):
        texture = pg.image.load('.\\venv\\fractal_Mandelbrutta\\textures\\0.jpg')
        self.texture_size = min(texture.get_size()) - 1
        self.texture_array = pg.surfarray.array3d(texture)

    def render(self):
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                c = (x - self.offset[0]) * self.zoom + 1j * (y - self.offset[1]) * self.zoom
                z = 0
                num_iter = 0
                for i in range(self.max_iter):
                    z = z ** 2 + c
                    if abs(z) > 2:
                        break
                    num_iter += 1
                col = int(self.texture_size * num_iter / self.max_iter)
                self.screen_array[x, y] = self.texture_array[col, col]

    def update(self):
        self.render()

    def draw(self):
        pg.surfarray.blit_array(self.screen, self.screen_array)