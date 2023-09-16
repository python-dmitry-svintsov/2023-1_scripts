#  Импорты основных библиотек
import pygame as pg
import numpy as np
from numba import njit
#  Импорты вспомогательных библиотек и системных утилит
from collections import deque
import sys
import math
#  import utils
from utils import SingeltonMeta
#  Импорты скриптов
from apps.lapi.program import Tunnel
from apps.voksel3d.program import VokselRoot
from apps.image_analizator.image_analizator import ImageAnalizator
from apps.image_analizator.image_game import PuzzleGame
from apps.fractal_Mandelbrutta.program_1 import Fractal_Mandelbrutta
from apps.pong.pong import Pong
from apps.puthfinder.program import PathFinder


class MainMenu(metaclass=SingeltonMeta):
    def __init__(self):
        #  Блок с глобальными переключателями
        # self.__program_switcher = False
        self.__menu_counter = 1
        self.__main_program = None
        self._request_to_exit = False
        # найстроки
        self.__screen_width = 1270
        self.__screen_height = 747
        self.settings()
        # списки для работы с меню
        self.__menu_list = self.get_menu()
        self.__list_level_counter = deque()  # стек-хранилище для кусочков меню (нужно для вложенных меню) в [-1][self.__currentlistcounter] всегда хранится текущее подменю для отрисовки
        self.__list_level_counter.append(self.__menu_list)
        self.__current_list_counter = 0  # счетчик для разделения меню если слишком длинное
        self.__current_menu()
        #  Инициализируем модуль pygame
        pg.init()
        self.__screen = pg.display.set_mode((self.__screen_width, self.__screen_height))
        self.__clock = pg.time.Clock()
        # start
        self.__start()

    def get_menu(self):
        menu_list = ['main menu',
                     {'name': 'Tunnel_Test',
                      'program': self.__program,
                      'class': Tunnel,
                      },
                     [
                         'voksel3d',
                         {
                             'name': 'numba',
                             'program': self.__program,
                             'class': VokselRoot,
                             'mode': 1
                         },
                         {
                             'name': 'white_noize',
                             'program': self.__program,
                             'class': VokselRoot,
                             'mode': 2
                         },
                         {
                             'name': 'taichi+',
                             'program': self.__program,
                             'class': VokselRoot,
                             'mode': 3
                         },
                         {
                             'name': 'numba+',
                             'program': self.__program,
                             'class': VokselRoot,
                             'mode': 4
                         }
                     ],
                     [
                         'image-analiz',
                         {
                             'name': 'analiz',
                             'program': self.__program,
                             'class': ImageAnalizator,
                         },
                         {
                             'name': 'puzzle-game',
                             'program': self.__program,
                             'class': PuzzleGame,
                         }
                     ],
                     [
                         'fractal',
                         {
                             'name': 'Python',
                             'program': self.__program,
                             'class': Fractal_Mandelbrutta,
                             'mode': 1
                         },
                         {
                             'name': 'numpy',
                             'program': self.__program,
                             'class': Fractal_Mandelbrutta,
                             'mode': 2
                         },
                         {
                             'name': 'numba',
                             'program': self.__program,
                             'class': Fractal_Mandelbrutta,
                             'mode': 3
                         },
                         {
                             'name': 'taichi',
                             'program': self.__program,
                             'class': Fractal_Mandelbrutta,
                             'mode': 4
                         },
                         {
                             'name': 'taichi-openGL',
                             'program': self.__program,
                             'class': Fractal_Mandelbrutta,
                             'mode': 5
                         }
                     ],
                     [
                         'pong game',
                         {
                             'name': 'mode1',
                             'program': self.__program,
                             'class': Pong,
                             'mode': 1
                         },
                         {
                             'name': 'mode2',
                             'program': self.__program,
                             'class': Pong,
                             'mode': 2
                         },
                         {
                             'name': 'sckvosh',
                             'program': self.__program,
                             'class': Pong,
                             'mode': 3
                         },
                     ],
                     [
                       'Path finder',
                         {
                             'name': 'алгоритм поиска в ширину',
                             'program': self.__program,
                             'class': PathFinder,
                             'mode': 1
                         },
                         {
                             'name': 'dejkstra',
                             'program': self.__program,
                             'class': PathFinder,
                             'mode': 2
                         },
                         {
                             'name': 'dejkstra + a*',
                             'program': self.__program,
                             'class': PathFinder,
                             'mode': 3
                         }
                     ],
                     {'name': 'Exit',
                     'program': self.__quit}
                     ]
        result = self.list_processing(menu_list)
        return result

    def __program(self, set: dict):
        self.__program_switcher = True
        self.__main_program = set.get('class', VokselRoot)(self, set)

    def __start(self):
        self.__run_program()

    def list_processing(self, my_list):
        ''''этот метод обрабатывает списко, если его длины больше чем заданы в настройках - делит его и добавляет маркеры для перемещения'''
        ''''тоже самое проделывается для встроенных меню - через рекурсию'''
        header = my_list[:1]
        list_body = my_list[1:]
        l_body = len(list_body)
        if l_body < self.__height_menu:
            result = list_body[:]
            for index, item in enumerate(list_body):
                if isinstance(item, list):
                    res = self.list_processing(item)
                    result[index] = res
            return [header + result]
        else:
            result = []
            start = 0
            stop = start + self.__height_menu - 2
            stop = min(stop, l_body)
            pices = math.ceil(l_body / self.__height_menu)
            for i in range(pices):
                cur_list = list_body[start:stop]
                if start != 0:
                    cur_list.insert(0, '<<<')
                if stop != l_body:
                    cur_list.append('>>>')
                start = stop
                stop += self.__height_menu - 3
                stop = min(stop, l_body)
                #  Если есть встроенное меню, вызываем рекурсию для его проверки и разбивки если потребуется
                for index, item in enumerate(cur_list):
                    if isinstance(item, list):
                        res = self.list_processing(item)
                        cur_list[index] = res
                result.append(header + cur_list)
            return result

    def __current_menu(self):
        ''''Получение текущего меню необходимого для отрисовки'''
        cur_list = self.__list_level_counter[-1][self.__current_list_counter]
        l = len(cur_list)
        at = np.array('', dtype=(np.unicode_, self.__len_line))  # это элемент списка - длиной в self.__len_line
        result_list = np.full(l, at)  # эта наш текущий списко для отрисовки
        for index, line in enumerate(cur_list):
            if isinstance(line, str):
                result_list[index] = line
            elif isinstance(line, list):
                result_list[index] = line[0][0] + '->'
            elif isinstance(line, dict):
                result_list[index] = line.get('name', 'unnamed')
        self.__current_list = result_list

    def settings(self):
        self.__fps = 60
        #  размер шрифтов
        self.__menu_font = 28
        self.dialog_font = 23
        #  Цвета шрифтов меню (оглавление, активный пункт меню, неактивный пункт меню)
        self.color_text_header = '#FFFFFF'
        self.color_text_active = '#FF00FF'
        self.color_text_inactive = '#E6E6FA'
        self.color_black = '#000000'
        self.color_red = '#DC143C'
        self.color_blue = '#0000CD'
        self.color_gray_lite = (77, 77, 77)
        self.color_contrast_1 = '#FFFFFF'
        self.color_contrast_2 = '#FFE4E1'
        # menu
        self.__len_of_menu_container = 200
        self.__len_line = 25
        self.__height_menu = 11
        # draw_elements
        self.__header_height = 10
        self.__footer_height = 25
        self.__menu_container_width = self.__screen_width // 4
        self.__menu_container_height = self.__screen_height // 2
        self.__fon_array = self.__fon_3d_array(np.full((self.__screen_width, self.__screen_height, 3), (10, 60, 80), dtype=np.uint8))
        self.menu_dialog_width = self.__menu_container_width // 1.2
        self.menu_dialog_height = self.__menu_container_height // 1.8
        self.__ticker_x = self.__screen_width  #  берущая строка


    #!!!! основной цикл, тут работает весь скрипты и все вложенные скрипты что запускаются как отдельные программы!!!
    def __run_program(self):
        while True:
            #  Если не активен скрипт то работает меню
            if not self.__main_program:
                self.__update()
                self.__draw()
            #  Если запущен скрипт то работает программа, внимание я вынес обработчик собитий в отдельный метод внутри класса!!!!
            else:
                self.__main_program.update()
                self.__main_program.draw()
                self.__main_program.events()

    def _exit_program(self):
        self.__main_program = False

    def __update(self):
        self.__control_menu()
        pg.display.flip()
        self.delta_time = self.__clock.tick(self.__fps)
        pg.display.set_caption(f'{self.__clock.get_fps()}:.1f')

    @staticmethod
    @njit
    def __fon_3d_array(array):
        step1 = 10
        step2 = 20
        x_len = len(array)
        y_len = len(array[0])
        for x in range(x_len):
            for y in range(y_len):
                if x % step1 == 0 and y % step1 == 0:
                    array[x][y] = (80, 80, 85)
                if x % step2 == 0 and y % step2 == 0:
                    array[x][y] = (100, 100, 100)
        return array

    def draw_window(self, x, y, width, height, color, frame_count):
        shadow = pg.Surface((width, height))
        shadow.set_alpha(100)
        shadow.fill((0, 0, 0))
        self.__screen.blit(shadow, (x + 20, y + 20))
        box = pg.Surface((width, height))
        box.fill(color)
        self.__screen.blit(box, (x, y))
        # draw frame
        padding = 10
        for i in range(frame_count):
            pg.draw.rect(self.__screen, self.color_contrast_1, (x + padding, y + padding, width - padding * 2, height - padding * 2), 1)
            padding += 5

    def draw_footer(self):
        pg.draw.rect(self.__screen, self.color_gray_lite, (0, self.__screen_height - self.__footer_height, self.__screen_width, self.__footer_height))
        self.draw_ticker()

    def draw_ticker(self):
        string = f'move Arrow_Up, Arrow_Down & Enter to navigate the menu. by Svintsov Dmytro 2023-07'
        self.__ticker_x -= 1
        if self.__ticker_x < -(len(string) * (self.dialog_font // 2.5)):
            self.__ticker_x = self.__screen_width
        font = pg.font.SysFont('comicksans', self.dialog_font)
        text = font.render(string, True, self.color_contrast_1)
        self.__screen.blit(text, (self.__ticker_x, self.__screen_height - self.dialog_font))

    def __draw(self):
        pg.surfarray.blit_array(self.__screen, self.__fon_array)
        self.__draw_menu()
        self.draw_footer()

    def __control_menu(self):
        for event in pg.event.get():
            lenght_current_menu = len(self.__list_level_counter[-1][self.__current_list_counter]) - 1
            self.__menu_counter = max(min(self.__menu_counter, lenght_current_menu), 1)
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.__menu_counter -= 1

            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.__menu_counter += 1

            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                elem = self.__list_level_counter[-1][self.__current_list_counter][self.__menu_counter]
                if isinstance(elem, list):
                    self.__list_level_counter.append(elem)
                    self.__current_list_counter = 0
                    self.__menu_counter = 1
                    self.__current_menu()
                elif isinstance(elem, dict):
                    self.__program_switcher = True
                    elem.get('program')(elem)
                elif elem == '>>>':
                    self.__current_list_counter += 1
                    self.__menu_counter = 1
                    self.__current_menu()
                elif elem == '<<<':
                    self.__current_list_counter -= 1
                    self.__current_menu()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:

                if len(self.__list_level_counter) == 1:
                    self.__quit(1)
                else:
                    self.__list_level_counter.pop()
                    self.__current_list_counter = 0
                    self.__current_menu()

    def __draw_menu(self):
        x_start = self.__screen_width // 2 - (self.__menu_container_width // 2) - 10
        y_start = self.__screen_height // 2 - (self.__menu_container_height // 2) - 10
        text_start = x_start + self.menu_dialog_width // 6
        ''''Draw box & suddow under menu window'''
        self.draw_window(x_start, y_start, self.__menu_container_width, self.__menu_container_height, self.color_gray_lite, 1)
        ''''Draw menu by self.__current_list'''
        font_1 = pg.font.SysFont('comicksans', self.__menu_font)
        font_2 = pg.font.SysFont('comicksans', self.__menu_font - 2)
        step = y_start + 40
        # self.__current_list = self.__current_menu()
        for index, item in enumerate(self.__current_list):
            if index == 0:
                text = font_1.render(f'{item.upper() + ":"}', True, self.color_text_header)
                self.__screen.blit(text, (text_start + 40, step))
                step += 10
            elif index == self.__menu_counter:
                text = font_2.render(f'{item}', True, self.color_text_active)
                self.__screen.blit(text, (text_start, step))
            else:
                text = font_2.render(f'{item}', True, self.color_text_inactive)
                self.__screen.blit(text, (text_start, step))
            step += self.__menu_font

    def get_value(self):
        return self.__screen, self.__clock, self.__screen_width, self.__screen_height, self.__fps

    def __draw_window_closed(self):
        """"отрисовываем окно закрытие прогарммы"""
        padding = 20
        x_start = self.__screen_width // 2 - (self.menu_dialog_width // 2) - 10
        y_start = self.__screen_height // 2 - (self.__menu_container_height // 2) - 10
        self.draw_window(x_start, y_start, self.menu_dialog_width, self.menu_dialog_height, self.color_red, 2)
        pg.draw.line(self.__screen, self.color_contrast_1, (x_start + padding, y_start + self.menu_dialog_height // 2),
                     (x_start + self.menu_dialog_width - padding, y_start + self.menu_dialog_height // 2), 2)
        font_1 = pg.font.SysFont('comicksans', self.dialog_font)
        text_1 = font_1.render('EXIT', True, (self.color_contrast_1))
        text_2 = font_1.render('Y / N', True, (self.color_contrast_1))
        self.__screen.blit(text_1, (x_start + self.menu_dialog_width // 2.5, y_start + self.menu_dialog_height // 4))
        self.__screen.blit(text_2, (x_start + self.menu_dialog_width // 2.5, y_start + (self.menu_dialog_height // 4) * 3))
        pg.display.flip()

    def _window_closed(self):
        while True:
            self.__draw_window_closed()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_y:
                    return True
                elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                    return False

    def __quit(self, settings):
        y = self._window_closed()
        if y:
            pg.quit()
            sys.exit()


if __name__ == '__main__':
    root = MainMenu()