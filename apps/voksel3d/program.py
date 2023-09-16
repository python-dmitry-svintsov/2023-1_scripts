import pygame as pg
#
from apps.voksel3d.player import Player
from apps.voksel3d.voksel_render import VoxelRender
from apps.voksel3d.voksel_render2 import VoxelRender2
from apps.voksel3d.voksel_render3 import VoxelRender3
from apps.voksel3d.voksel_render4 import VoxelRender4


class VokselRoot:
    def __init__(self, main, set):
        self.menu = main
        self.mode = set.get('mode', 1)
        self.screen, self.clock, self.width, self.height, self.fps = self.menu.get_value()
        self.settings()
        self.res = self.width, self.height
        self.player = Player()
        #  Начинаем новую игру
        self.new_sessions()

    def new_sessions(self):
        if self.mode == 1:
            self.voxel_render = VoxelRender(self)
        elif self.mode == 2:
            self.voxel_render = VoxelRender2(self)
        elif self.mode == 3:
            self.voxel_render = VoxelRender3(self)
        elif self.mode == 4:
            self.voxel_render = VoxelRender4(self)

    def settings(self):
        self.color_fon = '#000000'
        self.color_text = '#FFFFFF'
        self.font_size_1 = 40
        self.font_size_2 = 30
        self.color_1 = '#808080'
        self.color_2 = '#F5DEB3'
        self.color_3 = '#BC8F8F'

    def update(self):
        self.player.update()
        self.voxel_render.update()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'{self.clock.get_fps()}:.1f')

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

    def draw(self):
        self.voxel_render.draw()
        # end
        pg.display.flip()