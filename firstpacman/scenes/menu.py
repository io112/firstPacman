# Основы
import pygame
from pygame import Vector2
from firstpacman.constants import *
import firstpacman.debuger as debuger
from firstpacman.third_party.player.player import Player

# Меню
from firstpacman.third_party.button.button import Button
from firstpacman.scenes.activity import Activity

# Поле
from firstpacman.scenes.field import Field

# Семена
from firstpacman.scenes.seeds.objects.seed import *
from firstpacman.scenes.seeds.objects.bigSeed import *
from firstpacman.scenes.seeds.objects.fruit import *

# Энтити
from firstpacman.entities.pacman import Pacman
from firstpacman.entities.ghosts.targetGhost import TargetGhost
from firstpacman.entities.ghosts.wonderingGhost import WonderingGhost

class Menu(Activity):
    def __init__(self, game):
        super(Menu, self).__init__(game)
        self.player = Player()


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
        debuger.debuger = debuger.Debuger()

        # INIT
        main_field = Field(screen)
        main_field.init_field()
        # print(main_field.get_all_wall_rects())

        clyde_ghost = WonderingGhost(texture=pygame.image.load("images/orange_ghost.png"), speed=3, spawn_position=Vector2(clyde_spawnx, clyde_spawny))
        inky_ghost = WonderingGhost(texture=pygame.image.load("images/blue_ghost.png"), speed=3, spawn_position=Vector2(inky_spawnx, inky_spawny))
        pinky_ghost = TargetGhost(texture=pygame.image.load("images/purple_ghost.png"), speed=1, spawn_position=Vector2(pinky_spawnx, pinky_spawny), field=main_field)
        blinky_ghost = TargetGhost(texture=pygame.image.load("images/red_ghost.png"), speed=2, spawn_position=Vector2(blinky_spawnx, blinky_spawny), field=main_field)

        ghosts = []
        ghosts.append(clyde_ghost)
        ghosts.append(inky_ghost)
        ghosts.append(pinky_ghost)
        ghosts.append(blinky_ghost)

        pacman = Pacman(speed=2, position=Vector2(pac_spawnx, pac_spawny), ghosts=ghosts)

        seeds = pygame.sprite.Group()
        fruit_added = False

        font = pygame.font.Font('images/Comfortaa-SemiBold.ttf', 18)

        # Генерация семян
        for rect in main_field.get_all_seeds_coords():  # генерация зерен
            # print(rect)
            seed = Seed(screen, seeds)
            seed.set_coords(rect.x, rect.y, main_field)
        for seed in range(4):  # генерация особых зерен
            rnd_seed = random.choice(seeds.sprites())
            b_seed = BigSeed(screen, seeds)
            b_seed.reset_coords(rnd_seed)
            rnd_seed.kill()

        # GAME LOOP
        score = 0
        gameover = False
        while not gameover and not pacman.dead:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    gameover = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        debuger.DEBUG_MODE = not debuger.DEBUG_MODE

            text = font.render(str(score), True, (255, 46, 66))
            textRect = text.get_rect()
            textRect.x = 8
            textRect.y = 8

            if score >= 100 and not fruit_added:  # генерация фрукта при достижении очков
                rnd_seed = random.choice(seeds.sprites())
                fruit = Fruit(screen, seeds)
                fruit.reset_coords(rnd_seed)
                rnd_seed.kill()
                fruit_added = True

            # UPDATE
            pacman.update(seeds=seeds, ghosts=ghosts, field=main_field, events=events)
            score = pacman.score

            self.player.stop_menu_sound()
            self.player.play_game_sound()

            for ghost in ghosts:
                ghost.update(field=main_field, pacman=pacman)

            # DRAW
            screen.fill(bg_col)

            main_field.draw(screen)
            seeds.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen)
            pacman.draw(screen)

            debuger.debuger.draw(screen)

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
        self.player.stop_game_sound()
        self.player.play_menu_sound()
        self.screen.fill(bg_col)
        for button in self.buttons:
            button.update()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_on_click()
        pygame.display.flip()
