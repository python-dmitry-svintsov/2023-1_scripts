import random

import pygame as pg
from random import choice
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False
#  import utils & scripts
from apps.pong.game_constructor import Ball, Wall, PlayerPlatforms, MoovablePlatforms


class PongMode2:
    def __init__(self, game):
        # main secon:
        self.game = game
        self.screen = self.game.screen
        self.screen_width = self.game.screen_width
        self.screen_height = self.game.screen_height
        self.clock = self.game.clock
        self.fps = self.game.fps
        self.space = self.game.space
        # import components of game
        self.balls = Ball(self)
        self.walls = Wall(self)
        self.players = PlayerPlatforms(self)
        self.movable_platforms = MoovablePlatforms(self)
        # sounds
        self.ball_hit = pg.mixer.Sound('.\\venv\\apps\\pong\\sounds\\ball_hit.wav')
        self.goal = pg.mixer.Sound('.\\venv\\apps\\pong\\sounds\\goal.wav')
        # collision listener pymunk:
        self.collisions_listeners()
        # init game
        self.ways = [(-400, 400), (-400, -400), (400, -400), (400, 400)]
        self.padding_top = 60
        self.padding_bottom = 10
        self.font_size_score = self.game.text_size
        self.color_text_score = self.game.color_text
        self.font_size_dialog = self.game.font_size_dialog
        self.ball_raius = 10
        self.speed = 8e-1
        self.half_of_platforms_lenght = 45
        self.pos_a = self.screen_height // 2
        self.pos_b = self.screen_height // 2
        self.score_1 = 0
        self.score_2 = 0
        self.init()

    def init(self):
        self.player_1 = self.players.create_platforms((20, self.screen_height // 2), 1)
        self.player_2 = self.players.create_platforms((self.screen_width - 20, self.screen_height // 2), 2)
        self.ball = self.balls.create_ball(2, self.ball_raius, (self.screen_width // 2, self.screen_height // 2), 3)
        self.walls.create_wall((0, 0), (self.screen_width, 0), self.padding_top, 'darkslategray', 4)
        self.walls.create_wall((0, self.screen_height), (self.screen_width, self.screen_height), self.padding_bottom, 'darkslategray', 5)

    def collisions_listeners(self):
        self.collision = self.space.add_collision_handler(3, 1)
        self.collision.begin = self.sound
        self.collision = self.space.add_collision_handler(3, 2)
        self.collision.begin = self.sound
        self.collision = self.space.add_collision_handler(3, 4)
        self.collision.begin = self.sound
        self.collision = self.space.add_collision_handler(3, 5)
        self.collision.begin = self.sound
        self.collision = self.space.add_collision_handler(3, 6)
        self.collision.begin = self.sound
        self.collision = self.space.add_collision_handler(3, 7)
        self.collision.begin = self.sound

    def sound(self, a, b, c):
        self.ball_hit.play()
        x, y = self.ball.velocity
        self.ball.velocity = (x * 1.02, y * 1.02)
        # self.speed *= 1.02
        return True

    def control_game(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.pos_a = self.pos_a - (self.game.delta_time * self.speed)
        if key[pg.K_s]:
            self.pos_a = self.pos_a + (self.game.delta_time * self.speed)
        self.pos_a = min(max(self.pos_a, self.padding_top + self.half_of_platforms_lenght),
                         self.screen_height - (self.padding_bottom + self.half_of_platforms_lenght))
        self.player_1.position = (self.player_1.position[0], self.pos_a)
        if key[pg.K_UP]:
            self.pos_b = self.pos_b - (self.game.delta_time * self.speed)
        if key[pg.K_DOWN]:
            self.pos_b = self.pos_b + (self.game.delta_time * self.speed)
        self.pos_b = min(max(self.pos_b, self.padding_top + self.half_of_platforms_lenght),
                         self.screen_height - (self.padding_bottom + self.half_of_platforms_lenght))
        self.player_2.position = (self.player_2.position[0], self.pos_b)

    def draw_game_score(self):
        string_1 = f'score player1: {self.score_1}'
        string_2 = f'score player2: {self.score_2}'
        font = pg.font.SysFont('comicksans', self.font_size_score)
        text_1 = font.render(string_1, True, self.color_text_score)
        text_2 = font.render(string_2, True, self.color_text_score)
        self.screen.blit(text_1, (self.font_size_score, self.font_size_score // 2))
        self.screen.blit(text_2, (self.screen_width - 260, self.font_size_score // 2))

    def hit(self):
        self.goal.play()
        # self.speed = 8e-1
        self.ball.position = (self.screen_width // 2, self.screen_height // 2)
        self.ball.velocity = random.choice(self.ways)

    def check_game_score(self):
        if self.ball.position[0] > self.screen_width:
            self.score_1 += 1
            self.hit()
        elif self.ball.position[0] < 0:
            self.score_2 += 1
            self.hit()

    def update(self):
        self.movable_platforms.update()
        self.control_game()
        self.check_game_score()
        if self.score_1 > 9:
            self.game.request_to_stop = True
            self.game.winner = 1
            self.speed = 8e-1
            self.hit()
            self.score_1 = 0
            self.score_2 = 0
        elif self.score_2 > 9:
            self.game.request_to_stop = True
            self.game.winner = 2
            self.speed = 8e-1
            self.hit()
            self.score_1 = 0
            self.score_2 = 0

    def draw(self):
        # draw moovable_block:

        # draw walls:
        self.movable_platforms.draw()
        pg.draw.rect(self.screen, self.game.color_1, (0, 0, self.screen_width, self.padding_top))
        pg.draw.rect(self.screen, self.game.color_1,
                     (0, self.screen_height - self.padding_bottom, self.screen_width, self.screen_height))
        # draw elem
        self.players.draw()
        self.balls.draw()
        self.draw_game_score()