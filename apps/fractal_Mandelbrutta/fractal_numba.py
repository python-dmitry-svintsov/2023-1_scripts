import numba
import pygame as pg
import numpy as np
import numba as nb


class Fractal_3:
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
        texture = pg.image.load('.\\venv\\fractal_Mandelbrutta\\textures\\1.jpg')
        self.texture_size = min(texture.get_size()) - 1
        self.texture_array = pg.surfarray.array3d(texture)

    # numba.prange - это разделение потоков!!!
    @staticmethod
    @nb.njit(fastmath=True, parallel=True)
    def render(screen_array, screen_width, screen_height, zoom, offset, max_iter, texture_size, texture_array):
        for x in nb.prange(screen_width):
            for y in range(screen_height):
                c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
                z = 0
                num_iter = 0
                for i in range(max_iter):
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 > 4:
                        break
                    num_iter += 1
                col = int(texture_size * num_iter / max_iter)
                screen_array[x, y] = texture_array[col, col]
        return screen_array

    def update(self):
        self.screen_array = self.render(self.screen_array, self.screen_width, self.screen_height, self.zoom, self.offset,
                    self.max_iter, self.texture_size, self.texture_array)

    def draw(self):
        pg.surfarray.blit_array(self.screen, self.screen_array)