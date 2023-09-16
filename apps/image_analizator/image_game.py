import pygame as pg
import os
from random import choice, randrange
import numpy as np
#  Импорты скриптов


class PuzzleGame:
    def __init__(self, main, set):
        self.menu = main
        self.set = set
        self.screen, self.clock, self.screen_width, self.screen_height, self.fps = self.menu.get_value()

        # mouse control
        self.__first_clik_pos = (0, 0)
        self.__second_click_pos = (0, 0)
        self.__waiting_next_click = False
        self.__click_flag = False

        self.new_sessions()
        #  Начинаем новую sessions
        # self.new_sessions()

    def create_defoul_puzzle(self):
        img = pg.surfarray.t

    def load_image(self):
        path = os.path.abspath(os.path.join('venv', 'apps', 'image_analizator', 'resources', 'puzzle'))
        dir = os.listdir(path)
        file_name = choice(dir)
        self.image = pg.image.load(path + '\\' + file_name).convert_alpha()
        self.pices_list = []
        for y in range(self.y_len):
            for x in range(self.x_len):
                pice = self.image.subsurface(x * self.block_size, y * self.block_size,  self.block_size, self.block_size)
                self.pices_list.append(Puzzle(pice))

    def pices_arragment(self):
        self.dict_of_pices = dict()
        l = [i for i in range(len(self.pices_list))]
        for y in range(self.y_len):
            for x in range(self.x_len):
                index = choice(l)
                l.remove(index)
                self.pices_list[index].y = y
                self.pices_list[index].x = x
                self.dict_of_pices[x, y] = index
        # delete random puzzle:
        index = randrange(0, len(self.pices_list))
        delete_elem = self.pices_list[index]
        # dowload default pazzle:
        image = pg.image.load('.\\venv\\apps\\image_analizator\\resources\\picture\\default_puzzle.jpg').convert_alpha()
        self.black_elem = Puzzle(image)
        self.black_elem.x = delete_elem.x
        self.black_elem.y = delete_elem.y
        self.pices_list[index] = self.black_elem
        self.dict_of_pices[delete_elem.x, delete_elem.y] = None
        # print(len(list(self.dict_of_pices.values())))

    def new_sessions(self):
        self.settings()
        self.load_image()
        self.pices_arragment()
        self.get_graf()

    def settings(self):
        self.color_fon = '#000000'
        self.color_text = '#FFFFFF'
        self.text_size = 22
        self.h1_text_size = 26
        self.font_size_dialog = 28
        self.color_1 = '#808080'
        self.color_2 = '#F5DEB3'
        self.color_3 = '#BC8F8F'
        #
        self.block_size = 100
        self.x_len = 1000 // self.block_size
        self.y_len = 700 // self.block_size
        #
        self.ways = (-1, 0), (1, 0), (0, -1), (0, 1)
        self.graf = dict()
        # mooving puzzle
        self.mooving_flag = False
        self.speed = 2e-2
        self.current_puzzle = None
        self.start_pos = (self.x_len, self.y_len)
        self.end_pos = (self.x_len, self.y_len)

    def mouse_click(self):
        if self.__click_flag and not self.mooving_flag:
            self.__click_flag = False
            mouse_click_pos = (self.__first_clik_pos[0] // self.block_size, self.__first_clik_pos[1] // self.block_size)
            item_index = self.dict_of_pices.get(mouse_click_pos)
            ways = self.graf.get(mouse_click_pos)
            for way in ways:
                if self.dict_of_pices.get(way) == None:
                    elem = self.pices_list[item_index]
                    self.dict_of_pices[mouse_click_pos] = None
                    self.dict_of_pices[way] = item_index
                    #
                    self.black_elem.x, self.black_elem.y = self.x_len, self.y_len
                    self.mooving_flag = True
                    self.current_puzzle = elem
                    self.start_pos = mouse_click_pos
                    self.end_pos = way
                    # elem.x, elem.y = way
                    # self.black_elem.x, self.black_elem.y = mouse_click_pos
                    break

    def puzzle_moove(self):
        if self.mooving_flag:
            dx = self.end_pos[0] - self.start_pos[0]
            dy = self.end_pos[1] - self.start_pos[1]
            self.current_puzzle.x += dx * self.speed
            self.current_puzzle.y += dy * self.speed
            x_stop = abs(self.current_puzzle.x - self.end_pos[0])
            y_stop = abs(self.current_puzzle.y - self.end_pos[1])
            if x_stop < 0.1 and y_stop < 0.1:
                self.current_puzzle.x, self.current_puzzle.y = self.end_pos
                self.black_elem.x, self.black_elem.y = self.start_pos
                self.mooving_flag = False

    def get_ways(self, x, y):
        ways = []
        for elem in self.ways:
            dx = x + elem[0]
            dy = y + elem[1]
            if 0 <= dx < self.x_len and 0 <= dy < self.y_len:
                ways.append((dx, dy))
        return ways

    def get_graf(self):
        for y in range(self.y_len):
            for x in range(self.x_len):
                self.graf[x, y] = self.get_ways(x, y)

    def update(self):
        pg.display.flip()
        # self.control_game()
        self.mouse_click()
        self.puzzle_moove()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill(self.color_fon)
        # self.screen.blit(self.image, (0, 0))
        for item in self.pices_list:
            self.screen.blit(item.img, (item.x * self.block_size, item.y * self.block_size))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                y = self.menu._window_closed()
                if y:
                    self.menu._exit_program()
            # for mouse clicks
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                self.__first_clik_pos = pos
                self.__click_flag = True


class Puzzle:
    def __init__(self, img):
        self.x = 0
        self.y = 0
        self.img = img
