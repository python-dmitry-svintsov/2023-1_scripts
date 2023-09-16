import random

import pygame as pg
from random import choice
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False


class BasickUtils:
    def __init__(self, game):
        # pygame & pymunk section
        self.game = game
        self.screen = self.game.screen
        self.screen_width = self.game.screen_width
        self.screen_height = self.game.screen_height
        self.clock = self.game.clock
        self.fps = self.game.fps
        self.space = self.game.space
        # font, size, etc.
        self.font_size_3 = 28
        self.color_contrast = '#FFFFFF'
        self.color_1 = '#EE82EE'
        self.color_2 = '#AFEEEE'
        self.color_3 = '#B0C4DE'
        self.text_color = '#0000FF'


class RestartWindow(BasickUtils):
    def __init__(self, game):
        super().__init__(game)
        self.x_start = self.screen_width // 2 - (self.game.menu.menu_dialog_width // 2) - 10
        self.y_start = self.screen_height // 2 - (self.game.menu.menu_dialog_height // 2) - 10
        self.winner = 1
        self.color_closed_dindow = '#8A2BE2'

    def reset_window(self):
        """"draw reset window (if game finished)"""
        padding = 20
        self.game.menu.draw_window(self.x_start, self.y_start, self.game.menu.menu_dialog_width, self.game.menu.menu_dialog_height, self.color_closed_dindow, 2)
        pg.draw.line(self.screen, self.color_contrast, (self.x_start + padding, self.y_start + self.game.menu.menu_dialog_height // 2),
                     (self.x_start + self.game.menu.menu_dialog_width - padding, self.y_start + self.game.menu.menu_dialog_height // 2), 2)
        font_1 = pg.font.SysFont('comicksans', self.game.menu.dialog_font)
        text_1 = font_1.render(f'player{self.winner} win!', True, (self.color_contrast))
        text_2 = font_1.render('Wont to play again?', True, (self.color_contrast))
        text_3 = font_1.render('Y / N', True, (self.color_contrast))
        self.screen.blit(text_1, (self.x_start + self.game.menu.menu_dialog_width // 3,
                                  self.y_start + self.game.menu.menu_dialog_height // 4 - 15))
        self.screen.blit(text_2, (self.x_start + self.game.menu.menu_dialog_width // 3,
                                  self.y_start + self.game.menu.menu_dialog_height // 4 + 15))
        self.screen.blit(text_3,
                           (self.x_start + self.game.menu.menu_dialog_width // 2.5, self.y_start + (self.game.menu.menu_dialog_height // 4) * 3))
        pg.display.flip()

    def window_closed(self):
        while True:
            self.reset_window()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_y:
                    return True
                elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                    return False

    def restart(self, win):
        self.winner = win
        y = self.window_closed()
        if not y:
            self.game.menu._exit_program()


class Ball(BasickUtils):
    def __init__(self, game):
        super().__init__(game)
        self.ways = [(-400, 400), (-400, -400), (400, -400), (400, 400)]
        self.ball_raius = 10
        self.ball_color = self.game.game.color_2
        self.balls = []

    def create_ball(self, ball_mass, ball_radius, pos, collision_number):
        ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
        ball_body = pymunk.Body(ball_mass, ball_moment)
        ball_body.position = pos
        ball_body.velocity = random.choice(self.ways)
        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.density = 1
        ball_shape.elasticity = 1
        ball_shape.collision_type = 1
        self.space.add(ball_body, ball_shape)
        ball_shape.collision_type = collision_number
        self.balls.append(ball_body)
        return ball_body

    def update(self):
        pass

    def draw(self):
        for elem in self.balls:
            pg.draw.circle(self.screen, self.ball_color, elem.position, self.ball_raius)


class Wall(BasickUtils):
    def __init__(self, game):
        super().__init__(game)
        self.walls = list()
        self.wall_color = self.game.game.color_1

    def create_wall(self, from_, to_, thickness, color, collision_number=None):
        segment_shape = pymunk.Segment(self.space.static_body, from_, to_, thickness)
        segment_shape.color = pg.color.THECOLORS[color]
        segment_shape.density = 1
        segment_shape.elasticity = 1
        segment_shape.collision_type = 1
        self.space.add(segment_shape)
        self.walls.append((from_[0], from_[1] - thickness, to_[0], to_[1] + thickness))
        if collision_number:
            segment_shape.collision_type = collision_number

    def update(self):
        pass

    def draw(self):
        for elem in self.walls:
            pg.draw.rect(self.screen, self.wall_color, elem)


class PlayerPlatforms(BasickUtils):
    def __init__(self, game):
        super().__init__(game)
        self.player_thick = 20
        self.half_of_platforms_lenght = 45
        self.player_colors = self.game.game.color_3
        self.platforms_list = []

    def create_platforms(self, pos, collision_number=None):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = pos
        shape = pymunk.Segment(body, (0, -self.half_of_platforms_lenght), (0, self.half_of_platforms_lenght), self.player_thick // 2)
        shape.density = 1
        shape.elasticity = 1
        shape.collision_type = 1
        self.space.add(body, shape)
        self.platforms_list.append(body)
        if collision_number:
            shape.collision_type = collision_number
        return body

    def draw(self):
        for elem in self.platforms_list:
            pg.draw.rect(self.screen, self.player_colors,
                         (elem.position[0] - self.player_thick // 2,
                          elem.position[1] - self.half_of_platforms_lenght,
                          self.player_thick, self.half_of_platforms_lenght * 2))


class MoovablePlatforms(BasickUtils):
    def __init__(self, game):
        super().__init__(game)
        self.platforms_thick = 30
        self.platforms_lenght = self.screen_height // 2 - 25
        self.half_of_platform_lenght = self.platforms_lenght // 2
        self.wall_color = self.game.game.color_1
        self.platforms_list = []
        self.vector = -1
        self.init()

    def init(self):
        self.create_platforms((self.screen_width // 2, 0), 6)
        self.create_platforms((self.screen_width // 2, self.screen_height), 7)

    def create_platforms(self, pos, collision_number=None):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = pos
        shape = pymunk.Segment(body, (0, -self.half_of_platform_lenght), (0, self.half_of_platform_lenght),
                               self.platforms_thick // 2)
        shape.density = 1
        shape.elasticity = 1
        shape.collision_type = 1
        self.space.add(body, shape)
        self.platforms_list.append(body)
        if collision_number:
            shape.collision_type = collision_number

    def update(self):
        if self.platforms_list[0].position[1] + self.half_of_platform_lenght < self.game.padding_top:
            self.vector = 1
        elif self.platforms_list[1].position[1] - self.half_of_platform_lenght > self.screen_height - self.game.padding_bottom:
            self.vector = -1
        for elem in self.platforms_list:
            y = elem.position[1] + self.vector
            elem.position = elem.position[0], y

    def draw(self):
        for elem in self.platforms_list:
            y_top = elem.position[1] - self.half_of_platform_lenght
            y_bottom = elem.position[1] + self.half_of_platform_lenght
            y_top = max(y_top, 0)
            y_bottom = min(y_bottom, self.screen_height)
            pg.draw.rect(self.screen, self.wall_color, (self.screen_width // 2 - self.platforms_thick // 2, y_top, self.platforms_thick, y_bottom))
