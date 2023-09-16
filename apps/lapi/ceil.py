import pygame as pg


class Ceil():
    def __init__(self, app, x, y):
        self.app = app
        self.x, self.y = x, y
        self.size = self.app.tile_size
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.vizited = False
        self.color_ceil = (25, 25, 45)

    def draw(self):
        x, y = self.x * self.size, self.y * self.size
        if self.vizited:
            pg.draw.rect(self.app.screen, self.color_ceil, (x, y, self.size, self.size))
        if self.walls['top']:
            pg.draw.line(self.app.screen, self.app.color_white, (x, y), (x + self.size, y), 2)
        if self.walls['bottom']:
            pg.draw.line(self.app.screen, self.app.color_white, (x, y + self.size), (x + self.size, y + self.size), 2)
        if self.walls['left']:
            pg.draw.line(self.app.screen, self.app.color_white, (x, y), (x, y + self.size), 2)
        if self.walls['right']:
            pg.draw.line(self.app.screen, self.app.color_white, (x + self.size, y), (x + self.size, y + self.size), 2)


if __name__ == '__main__':
    pass