import random, pygame


class Object(pygame.sprite.Sprite):

    def __init__(self, picture=None):
        super().__init__()
        self.image = picture
        if picture is not None:
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

