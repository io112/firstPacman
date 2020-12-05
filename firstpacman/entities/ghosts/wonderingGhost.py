from random import random, randint

import pygame
from pygame import Vector2, Rect

from firstpacman.entities.ghosts.ghostBase import GhostBase
from firstpacman.constants import *
import firstpacman.debuger as global_vars

class WonderingGhost(GhostBase):
    def __init__(self, texture, speed, spawn_position):
        super().__init__(texture=texture, speed=speed, position=spawn_position)
        self.move_direction = Vector2(1, 0)
        self.prev_dir = Vector2(1, 0)
        self.target = self.position

    def update(self, field, pacman):
        self.move_direction = self.logic(field, pacman)
        # self.logic(pacman)
        self.velocity = self.move_direction * self.speed
        super().update(field=field)

    def logic(self, field, pacman):
        # Получить клетку, в которой находится призрак
        current_tile_rect = field.get_tile_from_point(self.position.x, self.position.y)
        global_vars.debuger.draw_rect(current_tile_rect) # Показать квадрат при дебаге

        # От сюда работаем в полевых координатах
        current_tile = field.get_field_coords_from_point(self.position.x, self.position.y)

        # Выбрать новую цель, если призрак дошел до текущей (Этот огромный IF проеверяет с учетом погрешности на скорость призрака)
        if self.is_target_too_far() or self.colliding or ((abs(self.target.x - self.position.x) <= self.speed) and (abs(self.target.y - self.position.y) <= self.speed)):
            new_target_on_field = self.update_move_dir(field, current_tile) + current_tile
            self.target = field.get_point_from_field_coords(round(new_target_on_field.x), round(new_target_on_field.y))
            self.target.x += 6
            self.target.y += 4
            global_vars.debuger.draw_rect(Rect(self.target.x, self.target.y, field.CELL_ACTUAL_SIZE, field.CELL_ACTUAL_SIZE))  # Показать квадрат при дебаге

        # Итогом является вектор по направлению к цели
        return (self.target - self.position).normalize()

    def update_move_dir(self, field, current_tile):
        # Определяем в каких сторонах есть стена
        possible_dirs = []
        if not field.field[round(current_tile.x + 1)][round(current_tile.y)]:
            dir_option = Vector2(1, 0)
            possible_dirs.append(dir_option)

        if not field.field[round(current_tile.x - 1)][round(current_tile.y)]:
            dir_option = Vector2(-1, 0)
            possible_dirs.append(dir_option)

        if not field.field[round(current_tile.x)][round(current_tile.y + 1)]:
            dir_option = Vector2(0, 1)
            possible_dirs.append(dir_option)

        if not field.field[round(current_tile.x)][round(current_tile.y - 1)]:
            dir_option = Vector2(0, -1)
            possible_dirs.append(dir_option)

        # НЕЛЬЗЯ ХОДИТЬ НАЗАД
        if (possible_dirs.__contains__(self.prev_dir)):
            possible_dirs.remove(self.prev_dir)

        index = randint(0, len(possible_dirs) - 1)
        # НЕЛЬЗЯ ХОДИТЬ НАЗАД
        self.prev_dir = possible_dirs[index] * -1
        return possible_dirs[index]