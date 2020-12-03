import pygame

from firstpacman.entities.movingObject import movingObject
from firstpacman.constants import *

from pygame import Vector2

class Pacman(movingObject):
    def __init__(self, speed, position):
        super().__init__(texture=pygame.image.load("images/pacman_circle.png"), speed=speed, position=position)
        self.move_direction = Vector2()

        self.clock = pygame.time.Clock()
        self.open_havalka_timer = True
        self.time = 0
        self.change_sprite = -1

    def update(self, field, events):
        self.update_movement(events)

        self.update_texture_timer()

        super().update(field)

    def update_movement(self, events):
        # Обновить вектор направления движения
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_direction.x -= 1
                    print('[MOVING] Left')

                if event.key == pygame.K_RIGHT:
                    self.move_direction.x += 1
                    print('[MOVING] Right')

                if event.key == pygame.K_UP:
                    self.move_direction.y -= 1
                    print('[MOVING] Up')

                if event.key == pygame.K_DOWN:
                    self.move_direction.y += 1
                    print('[MOVING] Down')

                # Обновить текстурку с новым направлением движения
                self.update_texture()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_direction.x += 1
                    print('[MOVING] Stopping Left')

                if event.key == pygame.K_RIGHT:
                    self.move_direction.x -= 1
                    print('[MOVING] Stopping Right')

                if event.key == pygame.K_UP:
                    self.move_direction.y += 1
                    print('[MOVING] Stopping Up')

                if event.key == pygame.K_DOWN:
                    self.move_direction.y -= 1
                    print('[MOVING] Stopping Down')

                # Обновить текстурку с новым направлением движения
                self.update_texture()

        # Нормализовать движение (чтобы пакман по горизонтали двигался с той же скоростью)
        if (self.move_direction != Vector2()):
            movement_normalized = self.move_direction.normalize()
            self.velocity.x = movement_normalized.x * self.speed
            self.velocity.y = movement_normalized.y * self.speed
        else:
            self.velocity = Vector2()

    def update_texture(self):
        if (self.move_direction.x > 0):
            self.texture = pygame.image.load("images/pacman_right.png")

        elif (self.move_direction.x < 0):
            self.texture = pygame.image.load("images/pacman_left.png")

        elif (self.move_direction.y > 0):
            self.texture = pygame.image.load("images/pacman_down.png")

        elif (self.move_direction.y < 0):
            self.texture = pygame.image.load("images/pacman_top.png")

        else:
            self.texture = pygame.image.load("images/pacman_circle.png")

    def update_texture_timer(self):
        if self.open_havalka_timer:
            self.time += self.clock.tick_busy_loop(60)

            if self.time > 300:
                if self.change_sprite > 0:
                    self.texture = pygame.image.load("images/pacman_circle.png")

                elif self.change_sprite < 0:
                    self.update_texture()

                self.change_sprite *= -1
                self.time = 0

    def draw(self, screen):
        super().draw(screen)