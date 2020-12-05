import pygame
from pygame import Vector2, Rect
from random import random, randint

from firstpacman.entities.ghosts.ghostBase import GhostBase

from firstpacman.constants import *
import firstpacman.debuger as global_vars

import pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class TargetGhost(GhostBase):
    def __init__(self, texture, speed, spawn_position, field):
        super().__init__(texture=texture, speed=speed, position=spawn_position)
        self.move_direction = Vector2(1, 0)
        self.prev_dir = Vector2(1, 0)
        self.target = self.position
        self.path = []

        self.field = field
        pathfinding_matrix = field.get_pathfinding_matrix()
        self.grid = Grid(matrix=pathfinding_matrix)

    def update(self, field, pacman):
        self.field = field
        self.move_direction = self.logic(pacman, field)
        self.velocity = self.move_direction * self.speed
        super().update(field=field)

    def logic(self, pacman, field):
        # Получить клетку, в которой находится призрак
        current_tile_rect = field.get_tile_from_point(self.position.x, self.position.y)
        global_vars.debuger.draw_rect(current_tile_rect)  # Показать квадрат при дебаге

        # От сюда работаем в полевых координатах
        current_tile = field.get_field_coords_from_point(self.position.x, self.position.y)

        # Выбрать новую цель, если призрак дошел до текущей (Этот огромный IF проеверяет с учетом погрешности на скорость призрака)
        if self.is_target_too_far() or self.colliding or ((abs(self.target.x - self.position.x) <= self.speed) and (
                abs(self.target.y - self.position.y) <= self.speed)):

            # Найти оптимальный путь к пакману
            self.path = self.pathfind_to(pacman.position.x, pacman.position.y)

            # Если слишком близко, то просто не идти
            if len(self.path) <= 1:
                return Vector2()

            # Первый элемент - положение призрака. Оно не нужно
            self.path.pop(0)

            # Идти к следующему
            new_target_on_field = self.path[0]

            # Установить новую цель
            self.target = field.get_point_from_field_coords(round(new_target_on_field[0]), round(new_target_on_field[1]))
            self.target.x += 6
            self.target.y += 4

            # Показать в дебагере цель
            global_vars.debuger.draw_rect(Rect(self.target.x, self.target.y, field.CELL_ACTUAL_SIZE, field.CELL_ACTUAL_SIZE))  # Показать квадрат при дебаге

        # Нарисовать в дебагере
        for i in range(1, len(self.path) - 1):
            modified_path = self.path.copy()
            if global_vars.DEBUG_MODE:
                for i in range(len(modified_path)):
                    modified_path[i] = (round(((modified_path[i][0] - 2) * field.CELL_ACTUAL_SIZE) + (field.CELL_ACTUAL_SIZE / 2)), round(((modified_path[i][1] - 2) * field.CELL_ACTUAL_SIZE) + (field.CELL_ACTUAL_SIZE / 2)))
                global_vars.debuger.draw_curved_line(modified_path, (43, 47, 58))

        # Итогом является вектор по направлению к цели
        result = Vector2()
        if (self.target != self.position):
            result = (self.target - self.position).normalize()
        return result

    def pathfind_to(self, x, y):
        self.grid.cleanup()
        start_pos_field = self.field.get_field_coords_from_point(self.position.x, self.position.y)
        end_pos_field = self.field.get_field_coords_from_point(x, y)

        start = self.grid.node(int(start_pos_field.x), int(start_pos_field.y))
        end = self.grid.node(int(end_pos_field.x), int(end_pos_field.y))

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, self.grid)

        return path