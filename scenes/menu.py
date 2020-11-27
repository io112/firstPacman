from third_party.button.button import Button
from scenes.activity import Activity
from constants import *
import pygame


class Menu(Activity):
    def __init__(self, game):
        super(Menu, self).__init__(game)

    def on_activate(self):
        self.inflate_buttons()

    def on_deactivate(self):
        self.buttons = list()

    def inflate_buttons(self):
        # to game button
        self.buttons.append(
            Button(pygame.rect.Rect(width // 2, height // 2 - height // 2.2, width // 2, height // 8),
                   self.to_game, 'scenes/image/play.png'))

        # exit button
        self.buttons.append(
            Button(pygame.rect.Rect(width // 2, height // 2, width // 2, height // 8),
                   Activity.exit_game, 'scenes/image/exit.png'))

        # stats button
        self.buttons.append(
            Button(pygame.rect.Rect(width // 2, height // 2 - height // 4.4, width // 2, height // 8),
                   self.to_stats, 'scenes/image/stats.png'))

    def to_game(self):
        # TODO: переход на field + self.on_deactivate()
        pass

    def to_stats(self):
        self.on_deactivate()
        self.game.set_scene(self.game.SCENE_STATS)
        self.game.scenes[self.game.SCENE_STATS].on_activate()

    def update(self, events):
        self.screen.fill(black)
        for button in self.buttons:
            button.update()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_on_click()
        pygame.display.flip()
