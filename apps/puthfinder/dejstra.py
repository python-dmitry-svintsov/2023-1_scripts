import pygame as pg
from collections import deque
from heapq import *


class Dejcstra:
    def __init__(self, program):
        self.program = program
        #  Цены
        self.price_1 = 1
        self.price_2 = 1
        self.price_3 = 1
        self.price_4 = 1
        self.ways = self.get_ways_and_prise()
        self.previous_click = tuple()
        self.current_click = tuple()
        self.graf = dict()
        self.get_graf()
        self.path = deque()
        #  Для отрисовки пути
        self.padding = self.program.blocks.padding
        self.scale = self.program.game_scale
        self.color = self.program.color_path
        self.color_area = self.program.color_area
        self.area_list = list()

    def get_ways_and_prise(self):
        return [self.price_1, -1, 0], [self.price_2, 0, -1], [self.price_3, 1, 0], [self.price_4, 0, 1]

    def get_nearly_coordinats(self, x, y):
        return [(price, (x + dx, y + dy)) for price, dx, dy in self.ways if (x + dx, y + dy) not in self.program.blocks.map]

    def get_graf(self):
        graf = {}
        for y, row in enumerate(self.program.blocks.block_list):
            for x, value in enumerate(row):
                if value < 8:
                    graf[(x, y)] = self.get_nearly_coordinats(x, y)
        # with open('.\graf.txt', 'r+') as file:
        #     for item in self.graf:
        #         result = str(item) + str(self.graf[item])
        #         file.write(result + '\n')
        return graf

    def dejkstra(self, start, goal):
        self.area_list.clear()

        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                break
            if cur_node in self.graf:
                next_nodes = self.graf[cur_node]

            self.area_list.append(cur_node)

            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    heappush(queue, (new_cost, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        return visited

    def get_path(self, start, goal):
        visited = self.dejkstra(start, goal)
        path = [goal]
        step = visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = visited[step]
        return path

    def update(self):
        if self.program.click_flag:
            start_pos = self.program.first_clik_pos
            end_pos = self.program.second_click_pos
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            self.price_1 = 0 if dx < 0 else 1
            self.price_2 = 0 if dy < 0 else 1
            self.price_3 = 0 if dx > 0 else 1
            self.price_4 = 0 if dy > 0 else 1
            self.ways = self.get_ways_and_prise()
            self.graf = self.get_graf()
            self.path = self.get_path(start_pos, end_pos)
            self.program.click_flag = False

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