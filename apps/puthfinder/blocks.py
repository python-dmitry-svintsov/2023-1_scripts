import pygame as pg
from random import randrange


class BlockField:
    def __init__(self, program):
        self.program = program
        self.block_list = self.get_block_list()
        self.scale = self.program.game_scale
        self.padding = 2
        self.map = dict()
        self.dict_map()
        self.color_1 = self.program.color_b1
        self.color_2 = self.program.color_b2

    def get_block_list(self):
        result_list = list()
        current_list = list()
        for i in range(self.program.height // self.program.game_scale):
            current_list = list()
            for j in range(self.program.width // self.program.game_scale):
                number = randrange(1, 10)
                current_list.append(number)
            result_list.append(current_list)
        return result_list

    def dict_map(self):
        for y, row in enumerate(self.block_list):
            for x, value in enumerate(row):
                if value > 7:
                    self.map[(x, y)] = value

    def draw(self):
        for pos in self.map:
            x, y = pos
            value = self.map[pos]
            if value == 9:
                pg.draw.rect(self.program.screen, (self.color_1), (
                x * self.scale + self.padding, y * self.scale + self.padding, self.scale - self.padding,
                self.scale - self.padding), border_radius=5)
            if value == 8:
                pg.draw.rect(self.program.screen, (self.color_2), (
                x * self.scale + self.padding, y * self.scale + self.padding, self.scale - self.padding,
                self.scale - self.padding), border_radius=5)

