import pygame as pg
from collections import deque


class Pathfinder:
    def __init__(self, program):
        self.program = program
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        self.previous_click = tuple()
        self.current_click = tuple()
        # self.switcher = False
        self.graf = dict()
        self.get_graf()
        self.path = deque()
        #  Для отрисовки пути
        self.padding = self.program.blocks.padding
        self.scale = self.program.game_scale
        self.color = self.program.color_path
        self.color_area = self.program.color_area
        self.area_list = list()

    def get_nearly_coordinats(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.program.blocks.map]

    def get_graf(self):
        for y, row in enumerate(self.program.blocks.block_list):
            for x, value in enumerate(row):
                if value < 8:
                    self.graf[(x, y)] = self.get_nearly_coordinats(x, y)
        # with open('.\graf.txt', 'r+') as file:
        #     for item in self.graf:
        #         result = str(item) + str(self.graf[item])
        #         file.write(result + '\n')

    def bfs(self, start, goal, graph):
        self.area_list.clear()

        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            if cur_node in self.graf:
                next_nodes = graph[cur_node]

            self.area_list.append(cur_node)

            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_path(self, start, goal):
        visited = self.bfs(start, goal, self.graf)
        path = [goal]
        step = visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = visited[step]
        return path

    def draw(self):
        for pos in self.area_list:
            x, y = pos
            pg.draw.rect(self.program.screen, (self.color_area), (
                x * self.scale + self.padding, y * self.scale + self.padding, self.scale - self.padding,
                self.scale - self.padding), border_radius=5)

        for pos in self.path:
            x, y = pos
            pg.draw.rect(self.program.screen, (self.color), (
                x * self.scale + self.padding, y * self.scale + self.padding, self.scale - self.padding,
                self.scale - self.padding), border_radius=5)

    def update(self):
        #  Для ускорения, ибо очень затратный алгоритм можна еще использовать декоратор lru.cash для кэшеирования но думаю это тут лишнее
        if self.program.click_flag:
            self.path = self.get_path(self.program.first_clik_pos, self.program.second_click_pos)
            self.program.click_flag = False