import pygame as pg
import math
#
from apps.fractal_Mandelbrutta.fractal import Fractal_1
from apps.fractal_Mandelbrutta.fractal_numpy import Fractal_2
from apps.fractal_Mandelbrutta.fractal_numba import Fractal_3
from apps.fractal_Mandelbrutta.fractal_taichi import Fractal_4
from apps.fractal_Mandelbrutta.fractal_taichi_open_gl import Fractal_5


class Fractal_Mandelbrutta:
    def __init__(self, main, set):
        self.main = main
        self.mode = set.get('mode', 1)
        self.screen, self.clock, self.screen_width, self.screen_height, self.fps = self.main.get_value()
        self.delta_time = 0
        self.settings()
        self.init()

    def init(self):
        if self.mode == 1:
            self.fractal = Fractal_1(self)
        elif self.mode == 2:
            self.fractal = Fractal_2(self)
        elif self.mode == 3:
            self.fractal = Fractal_3(self)
        elif self.mode == 4:
            self.fractal = Fractal_4(self)
        elif self.mode == 5:
            self.fractal = Fractal_5(self)


    def get_basik_values(self):
        return self.screen, self.screen_width, self.screen_height, self.delta_time

    def settings(self):
        self.color_fon = '#000000'
        self.color_text_red = '#FF0000'
        self.forn_size_1 = 40
        self.font_size_2 = 28
        self.color_1 = '#808080' #1
        self.color_2 = '#F5DEB3' #2
        self.color_3 = '#BC8F8F' #3

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps()}:.1f')
        self.fractal.update()

    def draw(self):
        self.screen.fill(self.color_fon)
        self.fractal.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                y = self.main._window_closed()
                if y:
                    self.main._exit_program()
            # for mouse clicks
            # elif event.type == pg.MOUSEBUTTONUP:
            #     pos = pg.mouse.get_pos()
            #     self.first_clik_pos = pos
            #     self.click_flag = True