import pygame as pg
import numpy as np
import taichi as ti


@ti.data_oriented
class Fractal_5:
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
        # taichi
        ti.init(arch=ti.opengl)
        self.screen_field = ti.Vector.field(3, ti.uint32, (self.screen_width, self.screen_height))
        self.texture_field = ti.Vector.field(3, ti.uint32, self.texture.get_size())
        self.texture_field.from_numpy(self.texture_array)

    def get_texture(self):
        self.texture = pg.image.load('.\\venv\\fractal_Mandelbrutta\\textures\\3.jpg')
        self.texture_size = min(self.texture.get_size()) - 1
        self.texture_array = pg.surfarray.array3d(self.texture).astype(dtype=np.uint32)

    @ti.kernel
    def render(self):
        for x, y in self.screen_field:
            c = ti.Vector([(x - self.offset[0]) * self.zoom, (y - self.offset[1]) * self.zoom])
            z = ti.Vector([0.0, 0.0])
            num_iter = 0
            for i in range(self.max_iter):
                z = ti.Vector([(z.x ** 2 - z.y ** 2 + c.x), (2 * z.x * z.y + c.y)])
                if z.dot(z) > 4:
                    break
                num_iter += 1
            col = int(self.texture_size * num_iter / self.max_iter)
            self.screen_field[x, y] = self.texture_field[col, col]

    def update(self):
        self.render()
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.screen, self.screen_array)