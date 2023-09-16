import pygame as pg
from collections import deque
from heapq import *


class AManhatten:
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
        return [(0, (x + dx, y + dy)) for dx, dy in self.ways if
                (x + dx, y + dy) not in self.program.blocks.map]

    def get_graf(self):
        for y, row in enumerate(self.program.blocks.block_list):
            for x, value in enumerate(row):
                if value < 8:
                    self.graf[(x, y)] = self.get_nearly_coordinats(x, y)

    def return_heuristick(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def dejkstra_a_(self, start, goal):
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
                    priority = new_cost + self.return_heuristick(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        return visited

    def get_path(self, start, goal):
        visited = self.dejkstra_a_(start, goal)
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
        if self.program.click_flag:
            self.path = self.get_path(self.program.first_clik_pos, self.program.second_click_pos)
            self.program.click_flag = False