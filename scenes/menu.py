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
            Button(380, 365, self.to_game, 'scenes/image/play.png'))

        # exit button
        self.buttons.append(
            Button(380, 477, Activity.exit_game, 'scenes/image/exit.png'))

        # stats button
        self.buttons.append(
            Button(380, 420, self.to_stats, 'scenes/image/stats.png'))
        
        self.buttons.append(
            Button(376, 230, self.on_logo,'scenes/image/logo.png'))

    def to_game(self):
        # TODO: переход на field + self.on_deactivate()
        pass

    def on_logo(self):
        # TODO: Пасхалка
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
