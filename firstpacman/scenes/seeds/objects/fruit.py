import random, pygame
from firstpacman.scenes.seeds.objects.seed import Seed

fruit = pygame.image.load("images/fruit.png")  # еще нет иллюстрации


class Fruit(Seed):
    def __init__(self, screen, group):
        super().__init__(screen, group, fruit)
        self.type = 'fruit'  # фрукт
        self.weight = 100



