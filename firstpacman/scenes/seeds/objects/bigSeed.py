import random, pygame
from firstpacman.scenes.seeds.objects.seed import Seed

big_seed = pygame.image.load("images/big_seed.png")


class BigSeed(Seed):
    def __init__(self, screen, group):
        super().__init__(screen, group, big_seed)
        self.type = 'big'  # большое зерно
        self.weight = 50


