import pygame
from firstpacman.entities.movingObject import movingObject
from firstpacman.constants import *

from pygame import Vector2

class Pacman(movingObject):
    def init(self, speed, position):
        super().init(texture=pygame.image.load("images/pacman_circle.png"), speed=speed, position=position)
        self.move_direction = Vector2()

        self.clock = pygame.time.Clock()
        self.open_havalka_timer = True
        self.time = 0
        self.change_sprite = -1

        self.dead = False
        self.score = 0
        self.hp = 3

        # Саунды пакмана. -- Егор
        self.init_sound = pygame.mixer.Sound("sounds/pacman_beginning.wav")
        self.havalka_sound = pygame.mixer.Sound("sounds/pacman_chomp.wav")
        self.eatfruit_sound = pygame.mixer.Sound("sounds/pacman_eatfruit.wav")
        self.eatghost_sound = pygame.mixer.Sound("sounds/pacman_eatghost.wav")
        self.death_sound = pygame.mixer.Sound("sounds/pacman_death.wav")

    def update(self, seeds, ghosts, field, events):
        # Движение
        self.update_movement(events)
        self.update_texture_timer()

        # Коллизии со специальными объектами и их обработка
        self.seeds_interact(seeds)
        self.ghosts_interact(ghosts)

        # Вызвать базовый update, который проверяет коллизии со стенами и все остальное
        super().update(field)

    # Семена
    def seeds_interact(self, seeds):
        # Просто ест семена всех типов, для начисление балов или эфектов будем проверять коллизию пакмана с семенем в
        # классе семян. pygame.sprite.spritecollide(self, list_of_all_object_groups[1], True) на всякий случай
        self.mask = pygame.mask.from_surface(self.texture)
        for seed in seeds:
            if pygame.sprite.collide_mask(self, seed):
                seeds.remove(seed)
                self.earn_points(seed)

    # Призраки
    def ghosts_interact(self, ghosts):
        colliding = self.check_ghosts_collision(ghosts)
        if colliding:
            self.die()

    def check_ghosts_collision(self, ghosts):
        for ghost in ghosts:
            # Я нашел это в интернете, но оно работает
            ghost_mask = pygame.mask.from_surface(ghost.texture)
            offset_x = int(ghost.position.x - self.position.x)
            offset_y = int(ghost.position.y - self.position.y)
            if self.mask.overlap(ghost_mask, (offset_x, offset_y)):
                return True

        return False

    # Движение
    def update_movement(self, events):
        # Обновить вектор направления движения
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_direction.x -= 1
                    print('[MOVING] Left')

                if event.key == pygame.K_RIGHT:
                    self.move_direction.x += 1
                    print('[MOVING] Right')

                if event.key == pygame.K_UP:
                    self.move_direction.y -= 1
                    print('[MOVING] Up')

                if event.key == pygame.K_DOWN:
                    self.move_direction.y += 1
                    print('[MOVING] Down')

                # Обновить текстурку с новым направлением движения
                self.update_texture()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_direction.x += 1
                    print('[MOVING] Stopping Left')

                if event.key == pygame.K_RIGHT:
                    self.move_direction.x -= 1
                    print('[MOVING] Stopping Right')

                if event.key == pygame.K_UP:
                    self.move_direction.y += 1
                    print('[MOVING] Stopping Up')

                if event.key == pygame.K_DOWN:
                    self.move_direction.y -= 1
                    print('[MOVING] Stopping Down')

                # Обновить текстурку с новым направлением движения
                self.update_texture()

        # Нормализовать движение (чтобы пакман по горизонтали двигался с той же скоростью)
        if (self.move_direction != Vector2()):
            movement_normalized = self.move_direction.normalize()
            self.velocity.x = movement_normalized.x * self.speed
            self.velocity.y = movement_normalized.y * self.speed
        else:
            self.velocity = Vector2()

    def update_texture(self):
        if (self.move_direction.x > 0):
            self.texture = pygame.image.load("images/pacman_right.png")
            # Обновить маску, так как мы поменяли текстурку
            self.mask = pygame.mask.from_surface(self.texture)

        elif (self.move_direction.x < 0):
            self.texture = pygame.image.load("images/pacman_left.png")
            # Обновить маску, так как мы поменяли текстурку
            self.mask = pygame.mask.from_surface(self.texture)

        elif (self.move_direction.y > 0):
            self.texture = pygame.image.load("images/pacman_down.png")
            # Обновить маску, так как мы поменяли текстурку
            self.mask = pygame.mask.from_surface(self.texture)

        elif (self.move_direction.y < 0):
            self.texture = pygame.image.load("images/pacman_top.png")
            # Обновить маску, так как мы поменяли текстурку
            self.mask = pygame.mask.from_surface(self.texture)

        else:
            self.texture = pygame.image.load("images/pacman_circle.png")
            # Обновить маску, так как мы поменяли текстурку
            self.mask = pygame.mask.from_surface(self.texture)

    def update_texture_timer(self):
        if self.open_havalka_timer:
            self.time += self.clock.tick_busy_loop(60)

            if self.time > 300:
                if self.change_sprite > 0:
                    self.texture = pygame.image.load("images/pacman_circle.png")
                    # Обновить маску, так как мы поменяли текстурку
                    self.mask = pygame.mask.from_surface(self.texture)

                elif self.change_sprite < 0:
                    self.update_texture()

                self.change_sprite *= -1
                self.time = 0

    # Вспомогательные
    def die(self):
        self.position = Vector2(pac_spawnx, pac_spawny)
        self.hp -= 1

        # Если у пакмана 0 жизней, то он мертв (логично)
        if self.hp <= 0:
            self.dead = True

    def earn_points(self, seed):
        # self.eatfruit_sound.play()
        self.score = self.score + seed.weight


    def draw(self, screen):
        super().draw(screen)