#  Импортируем главные фрейморки и библиотеки
import pygame as pg
#  Импортируем другие скрипты
from apps.puthfinder.blocks import BlockField
from apps.puthfinder.path_finder import Pathfinder
from apps.puthfinder.dejstra import Dejcstra
from apps.puthfinder.a_ import AManhatten


class PathFinder:
    def __init__(self, menu, set):
        self.menu = menu
        self.screen, self.clock, self.width, self.height, self.fps = menu.get_value()
        self.switcher = set.get('mode', 1)
        self.game_scale = 20
        self.color_b1, self.color_b2, self.color_path, self.color_area, self.color_fon = self.get_colors()
        # mouse_click:
        self.first_clik_pos = (0, 0)
        self.second_click_pos = (0, 0)
        self.wait_for_second_click = False
        self.click_flag = False
        #
        self.new_session()

    def get_colors(self):
        if self.switcher == 1:
            color_1 = (6, 60, 90)
            color_2 = (90, 6, 20)
            color_path = (90, 80, 7)
            color_path_area = (65, 90, 55)
            color_fon = (10, 20, 30)
        elif self.switcher == 2:
            color_1 = (40, 45, 90)
            color_2 = (60, 80, 45)
            color_path = (60, 4, 45)
            color_path_area = (80, 45, 85)
            color_fon = (20, 20, 20)
        elif self.switcher == 3:
            color_1 = (50, 50, 90)
            color_2 = (90, 90, 50)
            color_path = (80, 10, 20)
            color_path_area = (90, 50, 90)
            color_fon = (10, 20, 0)
        return color_1, color_2, color_path, color_path_area, color_fon

    def new_session(self):
        self.blocks = BlockField(self)
        if self.switcher == 1:
            self.path = Pathfinder(self)
        elif self.switcher == 2:
            self.path = Dejcstra(self)
        elif self.switcher == 3:
            self.path = AManhatten(self)

    def update(self):
        self.path.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps()}:.1f')

    def draw(self):
        self.screen.fill(self.color_fon)
        self.blocks.draw()
        self.path.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                y = self.menu._window_closed()
                if y:
                    self.menu._exit_program()
            # for mouse clicks
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                pos = (pos[0] // 20, pos[1] // 20)
                if not self.wait_for_second_click:
                    self.first_clik_pos = pos
                    self.wait_for_second_click = True
                else:
                    self.wait_for_second_click = False
                    self.second_click_pos = pos
                    self.click_flag = True