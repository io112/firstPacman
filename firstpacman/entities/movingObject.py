from pygame import Vector2
import pygame
from firstpacman.constants import *
import firstpacman.debuger as debuger

class movingObject():

    def __init__(self, texture, speed, position=Vector2()):
        self.texture = texture
        self.mask = pygame.mask.from_surface(self.texture)

        self.speed = speed
        self.colliding = False
        self.velocity = Vector2()
        self.position = position

        self.rect = self.texture.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def update(self, field):
        # Проверка коллизий
        self.check_collisions(field)

        # Сдвиг на переменную velocity (скорость с английского)
        self.position = self.position + self.velocity

        # Телепортация по краям карты
        self.check_if_out_of_screen()

        # Синхронизация положения объекта и тела
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def check_if_out_of_screen(self):
        if (self.position.x + self.rect.width <= 0):
            self.position.x = screen_height

        elif (self.position.x > screen_height):
            self.position.x = -self.rect.width

        if (self.position.y + self.rect.height <= 0):
            self.position.y = screen_width

        elif (self.position.y > screen_width):
            self.position.y = -self.rect.height

    def is_out_of_screen(self):
        if (self.position.x + self.rect.width <= 0):
            return True

        elif (self.position.x > screen_height):
            return True

        if (self.position.y + self.rect.height <= 0):
            return True

        elif (self.position.y > screen_width):
            return True

        return False

    def check_collisions(self, field):
        colliding_dirs = self.get_walls_collisions(field.get_all_wall_rects())

        # Если нет коллизий, то просто return
        if (colliding_dirs == []):
            return

        # Если есть коллизия по горизонтали, то скорость по горизонтали = 0
        if ((colliding_dirs.__contains__('left')) or (colliding_dirs.__contains__('right'))):
            self.velocity.x = 0

        # Если есть коллизия по вертикали, то скорость по вертикали = 0
        if ((colliding_dirs.__contains__('bottom')) or (colliding_dirs.__contains__('top'))):
            self.velocity.y = 0

    def get_walls_collisions(self, list_of_walls):
        collides_with = []

        # Пробегает по всем стенам и проверяет с ними коллизии
        for wall in list_of_walls:
            if (not collides_with.__contains__('right')) and (((self.rect.x + self.rect.width - self.velocity.x <= wall.x) and (self.rect.x + self.rect.width >= wall.x)) and ((self.rect.y + self.rect.height - 1 >= wall.y) and (self.rect.y + 1 <= wall.y + wall.height))):
                self.colliding = True
                collides_with.append('right')

                # Разрешает коллизию
                self.position.x = wall.x - self.rect.width

            elif (not collides_with.__contains__('left')) and ((self.rect.x - self.velocity.x >= wall.x + wall.width and self.rect.x <= wall.x + wall.width) and (self.rect.y + self.rect.height - 1 >= wall.y and self.rect.y + 1 <= wall.y + wall.height)):
                self.colliding = True
                collides_with.append('left')

                # Разрешает коллизию
                self.position.x = wall.x + wall.width

            elif (not collides_with.__contains__('bottom')) and ((self.rect.y + self.rect.height - self.velocity.y <= wall.y and self.rect.y + self.rect.height >= wall.y) and (self.rect.x + self.rect.width - 1 >= wall.x and self.rect.x + 1 <= wall.x + wall.width)):
                self.colliding = True
                collides_with.append('bottom')

                # Разрешает коллизию
                self.position.y = wall.y - self.rect.height

            elif (not collides_with.__contains__('top')) and ((self.rect.y - self.velocity.y >= wall.y + wall.height and self.rect.y <= wall.y + wall.height) and (self.rect.x - 1 + self.rect.width >= wall.x and self.rect.x + 1 <= wall.x + wall.width)):
                self.colliding = True
                collides_with.append('top')

                # Разрешает коллизию
                self.position.y = wall.y + wall.height

            else:
                self.colliding = False

        return collides_with

    def get_center(self):
        return Vector2(self.position.x + int(self.rect.width / 2), self.position.y + int(self.rect.height / 2))

    def draw(self, screen):
        screen.blit(self.texture, (self.position.x, self.position.y))

        if debuger.DEBUG_MODE:
            self.draw_hitbox(screen)
            self.draw_velocity_vector(screen)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, debuger.HITBOX_COLOR, self.rect, 1)

    def draw_velocity_vector(self, screen):
        pygame.draw.line(screen, debuger.VELOCITY_COLOR, self.get_center(), self.get_center() + self.velocity * debuger.VELOCITY_SCALE, 2)