import random, pygame
from firstpacman.scenes.seeds.objects.object import Object
from firstpacman.scenes.field import *


basic_seed = pygame.image.load("images/basic_seed.png")


class Seed(Object):
    def __init__(self, screen, group, picture=basic_seed):
        super().__init__(picture)  # теперь у Seed есть image, rect и mask. Просто чтобы самой не забыть
        self.type = 'basic'  # обычное зерно
        self.state = True  # видно/не видно
        self.weight = 10  # очки за съедение
        self.screen = screen
        self.add(group)  # добавление в свою группу спрайтов сразу по создании

    def set_coords(self, field_x, field_y, field): #получает номер ячейки поля и само поле
        self.rect.x = field_x * (field.CELL_ACTUAL_SIZE) + field.CELL_ACTUAL_SIZE / 2 - basic_seed.get_rect().height / 2 - 1
        self.rect.y = field_y * (field.CELL_ACTUAL_SIZE) + field.CELL_ACTUAL_SIZE / 2 - basic_seed.get_rect().height / 2 - 1

    def reset_coords(self, Seed_):
        self.rect.x = Seed_.rect.x
        self.rect.y = Seed_.rect.y

    def get_type(self):
        return self.type  # возвращает тип съеденого. на будущее, для возможности есть привидений

    def reverse_state(self):
        self.state = not self.state

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)
