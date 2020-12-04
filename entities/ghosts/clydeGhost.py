import pygame
from pygame import Vector2

from firstpacman.entities.ghosts.ghostBase import GhostBase

class Clyde(GhostBase):
    def __init__(self, speed, spawn_position):
        super().__init__(texture=pygame.image.load("images/blue_ghost.png"), speed=speed, position=spawn_position)
        self.move_direction = Vector2()

    def update(self, field, pacman):
        self.move_direction = self.logic(pacman)
        self.velocity = self.move_direction * self.speed
        super().update(field=field)

    def logic(self, pacman):
        return (pacman.position - self.position).normalize()