import random, pygame
from scenes.seeds.objects.Seed import Seed

fruit = pygame.image.load("images/fruit.png")  # еще нет иллюстрации


class Fruit(Seed):
    def __init__(self, screen, group):
        super().__init__(screen, group, fruit)
        self.type = 'fruit'  # фрукт
        self.weight = 100



