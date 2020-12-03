import pygame

class Object(pygame.sprite.Sprite):

    def __init__(self, picture = None):

        pygame.sprite.Sprite.__init__(self)
        self.image = picture
        if (picture != None):
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
