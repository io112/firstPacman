import sys
import pygame

from constants import *
from scenes.field import Field
from scenes.seeds.objects.Seed import *
from scenes.seeds.objects.BigSeed import *
from scenes.seeds.objects.Fruit import *
from entities.pacman import Pacman

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_dims)

    # INIT
    main_field = Field()
    main_field.init_field()
    # print(main_field.get_all_wall_rects())

    pacman = Pacman()
    pacman.draw(screen, 490, 500, 2)
    player = pygame.sprite.Group()
    player.add(pacman)

    seeds = pygame.sprite.Group()


    for rect in main_field.get_all_seeds_coords():
        print(rect)
        seed = Seed(screen, seeds)
        seed.set_coords(rect.x, rect.y, main_field)

    # GAME LOOP
    gameover = False
    while not gameover:
        for event in pygame.event.get():

            pacman.update(main_field.get_all_wall_rects(), seeds, event=event)

            if event.type == pygame.QUIT:
                gameover = True

        # block init_seeds_field started

        #print(pacman.rect.x , pacman.rect.y)
        #print(screen_width)
        pacman.update(main_field.get_all_wall_rects(), seeds, event=None)

        # UPDATE
        main_field.update()

        # DRAW
        screen.fill(bg_col)

        main_field.draw(screen)
        seeds.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
