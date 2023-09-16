import pygame as pg
import numpy as np
import math


class Player:
    def __init__(self):
        self.pos = np.array([200, 200], dtype=float)
        self.angle = math.pi / 4
        self.height = 250
        self.pitch = -80
        self.angle_vel = 0.05
        self.vel = 0.1
        self.pitch_velocity = 6

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_UP]:
            self.pitch += self.pitch_velocity
        if pressed_key[pg.K_DOWN]:
            self.pitch -= self.pitch_velocity

        if pressed_key[pg.K_LEFT]:
            self.angle -= self.angle_vel
        if pressed_key[pg.K_RIGHT]:
            self.angle += self.angle_vel

        if pressed_key[pg.K_q]:
            self.height += self.vel
        if pressed_key[pg.K_e]:
            self.height -= self.vel

        if pressed_key[pg.K_w]:
            self.pos[0] += self.vel * cos_a
            self.pos[1] += self.vel * sin_a
        if pressed_key[pg.K_s]:
            self.pos[0] -= self.vel * cos_a
            self.pos[1] -= self.vel * sin_a
        if pressed_key[pg.K_a]:
            self.pos[0] += self.vel * sin_a
            self.pos[1] -= self.vel * cos_a
        if pressed_key[pg.K_d]:
            self.pos[0] -= self.vel * sin_a
            self.pos[1] += self.vel * cos_a