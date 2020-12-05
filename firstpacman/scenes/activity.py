import pygame
from constants import *
import sys

'''
    a base class of all scenes

    update method must be in all classes extended from Activity. 
    it must be called every time in a cycle of activity_manager in game.py
'''


class Activity:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode(dims)
        self.font = pygame.font.SysFont(text_font, text_size)
        self.buttons = list()

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def update(self, events):
        pass

    @staticmethod
    def exit_game():
        sys.exit()
