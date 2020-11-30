from third_party.button.button import Button
from scenes.activity import Activity
from constants import *
import pygame
import sys
from constants import *
from scenes.field import Field
from scenes.seeds.objects.Seed import *
from scenes.seeds.objects.BigSeed import *
from scenes.seeds.objects.Fruit import *
from entities.pacman import Pacman
from entities.pinky import Pinky


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
            Button(376, 230, self.on_logo, 'scenes/image/logo.png'))

    def to_game(self):
        score = 0
        screen = pygame.display.set_mode(screen_dims)

        # INIT
        main_field = Field()
        main_field.init_field()
        # print(main_field.get_all_wall_rects())

        pacman = Pacman()
        pacman.draw(screen, pac_spawnx, pac_spawny, 2)
        player = pygame.sprite.Group()
        player.add(pacman)

        blue_ghost = Pinky(pygame.image.load("images/blue_ghost.png"))
        green_ghost = Pinky(pygame.image.load("images/green_ghost.png"))
        purple_ghost = Pinky(pygame.image.load("images/purple_ghost.png"))
        red_ghost = Pinky(pygame.image.load("images/red_ghost.png"))
        blue_ghost.draw(screen, blue_spawnx, blue_spawny, 1)
        green_ghost.draw(screen, green_spawnx, green_spawny, 1)
        purple_ghost.draw(screen, purple_spawnx, purple_spawny, 1)
        red_ghost.draw(screen, red_spawnx, red_spawnx, 1)

        blue_ghost.set_movement(True, 'right')
        blue_ghost.set_speed(4)

        green_ghost.set_movement(True, 'left')
        green_ghost.set_speed(4)

        blue_ghost.set_movement(True, 'down')
        blue_ghost.set_speed(4)

        red_ghost.set_movement(True, 'up')
        red_ghost.set_speed(4)

        ghosts = pygame.sprite.Group()
        ghosts.add(blue_ghost)
        ghosts.add(green_ghost)
        ghosts.add(purple_ghost)
        ghosts.add(red_ghost)

        seeds = pygame.sprite.Group()

        font = pygame.font.Font('images/Comfortaa-SemiBold.ttf', 18)

        for rect in main_field.get_all_seeds_coords():
            # print(rect)
            seed = Seed(screen, seeds)
            seed.set_coords(rect.x, rect.y, main_field)

        # GAME LOOP
        gameover = False
        gameover_by_button = False

        while not gameover_by_button and not gameover:
            for event in pygame.event.get():

                gameover = pacman.update([event, main_field, score], main_field.get_all_wall_rects(), seeds, ghosts, pacman)

                if event.type == pygame.QUIT:
                    gameover_by_button = True

            # block init_seeds_field started

            # print(pacman.rect.x , pacman.rect.y)
            # print(screen_width)

            text = font.render(str(score), True, (255, 46, 66))
            textRect = text.get_rect()
            textRect.x = 8
            textRect.y = 8

            # Если hp == 0 пакман, сразу завершаем игру (или вызываем обработку конца, имеется ввиду обновление списка рекордов
            gameover = pacman.update([None, main_field, score], main_field.get_all_wall_rects(), seeds, ghosts, pacman)
            score = pacman.sc       # В python как то геморно передовать переменную по ссылке, поэтому в пакмане хранится счет
            
            blue_ghost.update(main_field, main_field.get_all_wall_rects(), seeds, ghosts, pacman)
            red_ghost.update(main_field, main_field.get_all_wall_rects(), seeds, ghosts, pacman)
            green_ghost.update(main_field, main_field.get_all_wall_rects(), seeds, ghosts, pacman)
            purple_ghost.update(main_field, main_field.get_all_wall_rects(), seeds, ghosts, pacman)

            # DRAW
            screen.fill(bg_col)

            main_field.draw(screen)
            seeds.draw(screen)
            player.draw(screen)
            ghosts.draw(screen)

            screen.blit(text, textRect)

            pygame.display.flip()
            pygame.time.wait(10)        

        with open('records.txt', 'a') as f:
            f.write(str(score))
            f.write(str('\n'))

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
