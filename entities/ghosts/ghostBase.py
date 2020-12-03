import pygame, random
from pygame import Vector2

from firstpacman.entities.movingObject import movingObject
from firstpacman.constants import *

class GhostBase(movingObject):

    def __init__(self, texture, speed, position):
        super().__init__(texture=texture, speed=speed, position=position)

    def update(self, field):
        super().update(field)

    def draw(self, screen):
        super().draw(screen)
