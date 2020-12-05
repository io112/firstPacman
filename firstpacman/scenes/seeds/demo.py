import random, pygame
from scenes.seeds.objects.Seed import Seed
from scenes.seeds.objects.BigSeed import BigSeed
from scenes.seeds.objects.Fruit import Fruit


def demonstration():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    quit_screen = False

    while not quit_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_screen = True

        screen.fill((0, 0, 0))

        seeds = pygame.sprite.Group()

        seed = Seed(screen, seeds)
        seeds.draw(screen)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    demonstration()
