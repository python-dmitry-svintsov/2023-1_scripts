#  Импорты основных библиотек
import pygame as pg
import numpy as np
from random import choice
from pathlib import Path

#  Импорты вспомогательных библиотек и системных утилит
from utils import SingeltonMeta
#  Импoрты скриптов
from apps.lapi.ceil import Ceil

class Tunnel():
    def __init__(self, menu, set):
        self.menu = menu
        self.set = set
        self.screen, self.clock, self.screen_width, self.screen_height, self.fps = menu.get_value()
        self.settings()

    def settings(self):
        self.color_fon = (0, 0, 0)
        self.color_white = (255, 255, 255)
        self.color_current_ceil = (90,60,20)
        self.tile_size = 100
        self.cols, self.rows = self.screen_width // self.tile_size, self.screen_height // self.tile_size
        self.greed_ceils = [Ceil(self, col, row) for row in range(self.rows) for col in range(self.cols)]
        self.current_ceil = self.greed_ceils[0]
        self.next_ceil = self.current_ceil
        self.stack = []
        self.finished = False
        self.result_array = np.full((self.rows * 2 + 1, self.cols * 2 + 1), 1, dtype=np.uint8)

    def draw_curren_ceil(self):
        x, y = self.current_ceil.x * self.tile_size, self.current_ceil.y * self.tile_size
        pg.draw.rect(self.screen, self.color_current_ceil, (x + 2, y + 2, self.tile_size - 2, self.tile_size - 2))

    def check_ceil(self, x, y):
        find_index = x + y * self.cols
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return self.greed_ceils[find_index]

    def check_neighbords(self, ceil):
        neighbors = []
        top = self.check_ceil(ceil.x, ceil.y - 1)
        bottom = self.check_ceil(ceil.x, ceil.y + 1)
        left = self.check_ceil(ceil.x - 1, ceil.y)
        right = self.check_ceil(ceil.x + 1, ceil.y)
        if not isinstance(top, bool):
            if not top.vizited:
                neighbors.append(top)
        if not isinstance(bottom, bool):
            if not bottom.vizited:
                neighbors.append(bottom)
        if not isinstance(left, bool):
            if not left.vizited:
                neighbors.append(left)
        if not isinstance(right, bool):
            if not right.vizited:
                neighbors.append(right)
        return choice(neighbors) if neighbors else False

    def remoove_walls(self):
        x = self.current_ceil.x * 2 + 1
        y = self.current_ceil.y * 2 + 1
        dx = self.current_ceil.x - self.next_ceil.x
        if dx == 1:
            self.result_array[y][x - 1] = 0
            self.current_ceil.walls['left'] = False
            self.next_ceil.walls['right'] = False
        elif dx == -1:
            self.result_array[y][x + 1] = 0
            self.current_ceil.walls['right'] = False
            self.next_ceil.walls['left'] = False
        dy = self.current_ceil.y - self.next_ceil.y
        if dy == 1:
            self.result_array[y - 1][x] = 0
            self.current_ceil.walls['top'] = False
            self.next_ceil.walls['bottom'] = False
        elif dy == -1:
            self.result_array[y + 1][x] = 0
            self.current_ceil.walls['bottom'] = False
            self.next_ceil.walls['top'] = False

    def save_result(self):
        my_dir = Path(__file__).resolve().parent
        with open(str(my_dir) + '\\' + 'map.txt', 'w+') as file:
            for row in range(len(self.result_array)):
                for col in range(len(self.result_array[0])):
                    file.write(str(self.result_array[row][col]))
                    if col < len(self.result_array[0]) - 1:
                        file.write(' ')
                if row < len(self.result_array) - 1:
                    file.write('\n')


    def update(self):
        pg.display.flip()
        if not self.finished:
            self.current_ceil.vizited = True
            #  ------------------------------------------------------------------------------------------------
            x = self.current_ceil.x
            y = self.current_ceil.y
            self.result_array[y * 2 + 1][x * 2 + 1] = 0
            #  ------------------------------------------------------------------------------------------------
            self.next_ceil = self.check_neighbords(self.current_ceil)
            if self.next_ceil:
                self.stack.append(self.current_ceil)
                self.remoove_walls()
                self.current_ceil = self.next_ceil
            elif self.stack:
                self.current_ceil = self.stack.pop()
            else:
                self.finished = True
                self.save_result()

        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps()}:.1f')

    def draw(self):
        self.screen.fill(self.color_fon)
        [ceil.draw() for ceil in self.greed_ceils]
        self.draw_curren_ceil()

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


if __name__ == '__main__':
    pass