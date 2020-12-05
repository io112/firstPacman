import pygame
import sys
from scenes.menu import Menu
from scenes.stats import Stats

'''
    activity manager is a game loop
'''
is_working = True


class Game:
    SCENE_MENU = 0
    SCENE_STATS = 1
    SCENE_GAME = 2  # game activity id
    current_scene_index = SCENE_MENU

    def __init__(self):
        self.scenes = [Menu(self), Stats(self)]  # TODO: add field activity
        self.scenes[self.SCENE_MENU].on_activate()

    def set_scene(self, scene_index):
        self.current_scene_index = scene_index

    def activity_manager(self):
        while is_working:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self.scenes[self.current_scene_index].update(events)
            pygame.time.wait(10)
