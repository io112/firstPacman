import random, pygame
from scenes.seeds.objects.Seed import Seed

big_seed = pygame.image.load("images/big_seed.png")  # еще нет иллюстрации


class BigSeed(Seed):
    def __init__(self, screen, group):
        super().__init__(screen, group)
        self.type = 'big'  # большое зерно
        self.weight = 50


