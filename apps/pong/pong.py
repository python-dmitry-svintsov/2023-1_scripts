import pygame as pg
#  Импoрты скриптов программ что запускаются из меню
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False
#  Импорты скриптов
# from pong_mode_1 import PongMode1
from apps.pong.pong_1 import PongMode1
from apps.pong.pong_2 import PongMode2
from apps.pong.scvosh import ScvoshMode1
from apps.pong.game_constructor import RestartWindow


class Pong:
    def __init__(self, main, set):
        self.menu = main
        self.mode = set.get('mode', 1)
        self.screen, self.clock, self.screen_width, self.screen_height, self.fps = self.menu.get_value()
        self.winner = 0
        self.request_to_stop = False
        self.settings()
        # Инициализируем библиотеку pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = 0, 0
        self.restart_window = RestartWindow(self)
        #  Начинаем новую игру
        self.new_sessions()

    def new_sessions(self):
        # select game_mode
        if self.mode == 1:
            self.game = PongMode1(self)
        elif self.mode == 2:
            self.game = PongMode2(self)
        elif self.mode == 3:
            self.game = ScvoshMode1(self)

    def settings(self):
        self.color_fon = '#000000'
        self.color_text = '#FFFFFF'
        self.text_size = 40
        self.font_size_dialog = 28
        self.color_1 = '#808080'
        self.color_2 = '#F5DEB3'
        self.color_3 = '#BC8F8F'



    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps()}:.1f')
        #
        self.space.step(1 / self.fps)
        #
        self.game.update()

    def draw(self):
        self.screen.fill(self.color_fon)
        # self.space.debug_draw(self.draw_options)
        self.game.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                y = self.menu._window_closed()
                if y:
                    self.menu._exit_program()
        if self.request_to_stop:
            self.request_to_stop = False
            self.restart_window.restart(self.winner)
