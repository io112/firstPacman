from firstpacman.entities.ghosts.ghostBase import GhostBase
import pygame
from pygame import Vector2

class Clyde(GhostBase):
    def __init__(self, speed, spawn_position):
        super().__init__(texture=pygame.image.load("images/blue_ghost.png"), speed=speed, position=spawn_position)