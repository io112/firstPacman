import pygame
from constants import *


class Button:
    """
        self.rect = button rectangle
        self.function = what button does after click
    """

    def __init__(self, rect, function, text):
        self.rect = pygame.Rect(rect)
        self.function = function
        self.text = text
        self.screen = pygame.display.set_mode(dims)

    # checks whether button clicked or not
    def check_on_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.function()

    # update is called every time in a loop
    def update(self):
        self.screen.fill(black, self.rect)
        self.screen.fill(button_color, self.rect.inflate(-4, -4))
        text_rect = self.text.get_rect(center=self.rect.center)
        self.screen.blit(self.text, text_rect)
