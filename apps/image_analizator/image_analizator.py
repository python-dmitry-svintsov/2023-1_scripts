#  Импoрты скриптов программ что запускаются из меню
import numba
from numba.typed.typeddict import Dict
from numba import int8, int32
import pygame as pg
import numpy as np
import numba as nb
#  Импорты скриптов
from utils import time_decorator


class ImageAnalizator:
    def __init__(self, main, set):
        self.menu = main
        self.set = set
        self.screen, self.clock, self.screen_width, self.screen_height, self.fps = self.menu.get_value()
        self.screen_array = np.full((self.screen_width, self.screen_height, 3), (0, 0, 0), dtype=np.uint8)
        self.color_dict = Dict.empty(key_type=numba.types.UniTuple(int8, 3), value_type=int32)
        self.result_array = np.full(6, 0, dtype=np.uint16)
        self.color_array = np.array(['red:', 'yellow:', 'green:', 'white-blue:', 'dark-blue:', 'pink:'], dtype=[('colors', 'U12')])
        self.new_sessions()
        #  Начинаем новую sessions
        # self.new_sessions()

    @time_decorator
    def image_loader(self):
        image = pg.image.load('.\\venv\\apps\\image_analizator\\resources\\picture\\birds_1.jpg')
        color_map = pg.surfarray.array3d(image)
        x_len = len(color_map)
        y_len = len(color_map[0])
        if x_len > self.screen_width or y_len > self.screen_height:
            for x in range(x_len):
                for y in range(y_len):
                    if x < self.screen_width:
                        if y < self.screen_height:
                            self.screen_array[x][y] = color_map[x][y]
        else:
            x_displacment = (self.screen_width - x_len) // 2
            y_displacment = (self.screen_height - y_len) // 2
            for x in range(x_len):
                for y in range(y_len):
                    self.screen_array[x + x_displacment][y + y_displacment] = color_map[x][y]
        self.color_dict = self.image_analizator(color_map, self.color_dict)
        self.color_value = list(self.color_dict.values())

    @staticmethod
    @time_decorator
    @numba.njit
    def image_analizator(screen_array, result_dict):
        x_len = len(screen_array)
        y_len = len(screen_array[0])
        for x in range(x_len):
            for y in range(y_len):
                array = screen_array[x][y]
                r = 0 if array[0] / 256 < 0.5 else 1
                g = 0 if array[1] / 256 < 0.5 else 1
                b = 0 if array[2] / 256 < 0.5 else 1
                color_tupple = (r, g, b)
                if not color_tupple in result_dict:
                    result_dict[color_tupple] = 0
                else:
                    result_dict[color_tupple] += 1
        return result_dict

    def new_sessions(self):
        self.settings()
        self.image_loader()

    def settings(self):
        self.color_fon = '#000000'
        self.color_text = '#FFFFFF'
        self.text_size = 22
        self.h1_text_size = 26
        self.font_size_dialog = 28
        self.color_1 = '#808080'
        self.color_2 = '#F5DEB3'
        self.color_3 = '#BC8F8F'

    def draw_result(self):
        font_1 = pg.font.SysFont('comicksans', self.h1_text_size)
        font_2 = pg.font.SysFont('comicksans', self.text_size)
        pg.draw.rect(self.screen, self.color_fon, (20, 20, 170, 200))
        step = 30
        header = font_1.render(f'COLORS:', True, self.color_text)
        self.screen.blit(header, (30, step))
        step += 15
        for i in range(len(self.color_value) - 1):
            step += 25
            string = self.color_array['colors'][i]
            text1 = font_2.render(f'{string}', True, self.color_text)
            text2 = font_2.render(f'{self.color_value[i]}', True, self.color_text)
            self.screen.blit(text1, (20, step))
            self.screen.blit(text2, (115, step))

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill(self.color_fon)
        pg.surfarray.blit_array(self.screen, self.screen_array)
        self.draw_result()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                y = self.menu._window_closed()
                if y:
                    self.menu._exit_program()
            # for mouse clicks
            # elif event.type == pg.MOUSEBUTTONUP:
            #     pos = pg.mouse.get_pos()
            #     self.first_clik_pos = pos
            #     self.click_flag = True