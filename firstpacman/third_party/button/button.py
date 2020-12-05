import pygame
from firstpacman.constants import *


class Button:
    """
        self.rect = button rectangle
        self.function = what button does after click
    """

    def __init__(self, x, y, function, name_of_picture):
        self.pic = name_of_picture
        self.pict = pygame.image.load(self.pic)
        self.rect = self.pict.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.function = function
        self.screen = pygame.display.set_mode(dims)

    # checks whether button clicked or not
    def check_on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.function()

    # update is called every time in a loop
    def update(self):
        self.screen.blit(self.pict, self.rect)
