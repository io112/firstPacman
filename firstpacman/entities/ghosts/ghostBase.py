import pygame, random
from pygame import Vector2

from firstpacman.entities.movingObject import movingObject
from firstpacman.constants import *

class GhostBase(movingObject):

    def __init__(self, texture, speed, position):
        super().__init__(texture=texture, speed=speed, position=position)

        self.vulnurable = False

    def update(self, field):
        if self.vulnurable:
            pass
        super().update(field)

    def is_target_too_far(self):
        return (self.target - self.position).length() > screen_height / 2

    def draw(self, screen):
        super().draw(screen)
