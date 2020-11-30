from scenes.activity import Activity
from constants import *
from third_party.button.button import Button
import pygame, os

# Приятель, я немного подправил твой код, надеюся те норм...

class Stats(Activity):
    def __init__(self, game):
        super(Stats, self).__init__(game)
        self.records = list()
        self.is_empty = False

    def on_activate(self):
        #if len(self.records) == 0:
        self.read_records()
        self.inflate_buttons()

    def on_deactivate(self):
        self.buttons = list()

    def read_records(self):
        '''
        f = open('records.txt', 'r')
        for line in f:
            self.records.append(int(line))
        f.close()
        if len(self.records) == 0:
            self.records.append('Records will be here')
        else:
            self.records.sort(reverse=True)

        '''
        if (not os.path.isfile('records.txt')):
            self.is_empty = True
            with open('records.txt', 'a+') as f:
                pass
            print('empty')

        else:
            with open('records.txt', 'r') as f:
                for i in f:
                    self.records.append(int(i[:len(i) - 1]))
            print(self.records)
            self.records = sorted(set(self.records), key=lambda d: self.records.index(d))
            self.records.sort(reverse=True)
            self.is_empty = False


    def draw_records(self):

        number_of_records = 10
        if (len(self.records) <= 10):
            number_of_records = len(self.records)

        if (self.is_empty):
            text = self.font.render('Records will be here', True, text_color)
            text_rect = text.get_rect(center=(width // 2 + 100 + width // 13 + 70, 40 + 20 + 10 + 70))
            self.screen.blit(text, text_rect)

        else:
            for i in range(number_of_records):
                pygame.draw.rect(self.screen, button_color, (width // 2 + 70, i * 40 + 10 + 70, 100, 40), 2)
                text = self.font.render(str(i + 1), True, text_color)
                text_rect = text.get_rect(center=(width // 2 + width // 13 + 70, i * 40 + 20 + 10 + 70))
                self.screen.blit(text, text_rect)
                pygame.draw.rect(self.screen, button_color, (width // 2 + 100 + 70, i * 40 + 10 + 70, 100, 40), 2)
                text = self.font.render(str(self.records[i]), True, text_color)
                text_rect = text.get_rect(center=(width // 2 + 100 + width // 13 + 70, i * 40 + 20 + 10 + 70))
                self.screen.blit(text, text_rect)

    def inflate_buttons(self):
        # back to menu button
        text = self.font.render('Back', True, text_color)
        self.buttons.append(
            Button(0,0,
                   self.to_menu, "scenes/image/exit.png"))

    def to_menu(self):
        self.on_deactivate()
        self.game.set_scene(self.game.SCENE_MENU)
        self.game.scenes[self.game.SCENE_MENU].on_activate()

    def update(self, events):
        self.screen.fill(black)
        for button in self.buttons:
            button.update()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_on_click()
        self.draw_records()
        pygame.display.flip()
