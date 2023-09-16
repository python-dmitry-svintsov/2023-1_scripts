import pygame as pg
import numpy as np


class Fractal_2:
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
        # numpy
        self.x = np.linspace(0, self.screen_width, num=self.screen_width, dtype=np.float32)
        self.y = np.linspace(0, self.screen_height, num=self.screen_height, dtype=np.float32)

    def get_texture(self):
        texture = pg.image.load('.\\venv\\fractal_Mandelbrutta\\textures\\1.jpg')
        self.texture_size = min(texture.get_size()) - 1
        self.texture_array = pg.surfarray.array3d(texture)

    def render(self):
        x = (self.x - self.offset[0]) * self.zoom
        y = (self.y - self.offset[1]) * self.zoom
        c = x + 1j * y[:, None]

        num_iter = np.full(c.shape, self.max_iter)
        z = np.empty(c.shape, np.complex64)
        for i in range(self.max_iter):
            mask = (num_iter == num_iter)
            z[mask] = z[mask] ** 2 + c[mask]
            num_iter[mask & (np.abs(z) > 2.0)] = i + 1
            # num_iter[mask & (z.real ** 2 + z.imag ** 2 > 4.0)] = i + 1

        col = (num_iter.T * self.texture_size / self.max_iter).astype(np.uint8)
        self.screen_array = self.texture_array[col, col]

    def update(self):
        self.render()

    def draw(self):
        pg.surfarray.blit_array(self.screen, self.screen_array)