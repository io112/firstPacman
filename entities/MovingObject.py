from entities.object import Object
from constants import *
import random, pygame

class movingObject(Object):

    def __init__(self, texture):
        super().__init__(texture)
        self.type = 'moveobject'
        self.conspeed = 0  # Скорость одинакова для всех направлений
        self.speed = {'speed_l': -self.conspeed, 'speed_r': self.conspeed, 'speed_u': -self.conspeed, 'speed_d': self.conspeed}
        self.move_dir = 'none'
        self.prev_move_dir = 'none'
        self.is_moving = False
        self.last_loc_cell = 'none'
        self.colliding = False

    def set_speed(self, speed):
        self.conspeed = speed
        self.speed = {'speed_l': -self.conspeed, 'speed_r': self.conspeed, 'speed_u': -self.conspeed, 'speed_d': self.conspeed}

    def set_movement(self, move_status, direction = 'not change'):

        self.is_moving = move_status

        if (direction != 'not change'):
            self.move_dir = direction

        if (self.move_dir != self.prev_move_dir):
            self.prev_move_dir = self.move_dir


    def move(self):

        dirs = ['left', 'right', 'up', 'down']

        if (self.is_moving):

            if (self.move_dir == dirs[0]):
                if (not self.speed['speed_l']):     #Проверяет на нулевую скорость... не уверен, что нужно
                    self.set_movement(False)
                else:
                    self.rect.move_ip(self.speed['speed_l'], 0)

            elif (self.move_dir == dirs[1]):
                if (not self.speed['speed_r']):
                    self.set_movement(False)
                else:
                    self.rect.move_ip(self.speed['speed_r'], 0)


            elif (self.move_dir == dirs[2]):
                if (not self.speed['speed_u']):
                    self.set_movement(False)
                else:
                    self.rect.move_ip(0, self.speed['speed_u'])

            elif (self.move_dir == dirs[3]):
                if (not self.speed['speed_d']):
                    self.set_movement(False)
                else:
                    self.rect.move_ip(0, self.speed['speed_d'])



    def walls_collision(self, list_of_walls):

        for wall in list_of_walls:

            #print(self.rect.x, self.rect.y, wall.x, wall.y)

            if ((self.rect.x + self.rect.width - self.speed['speed_r'] <= wall.x and self.rect.x + self.rect.width >= wall.x) and (self.rect.y + self.rect.height >= wall.y and self.rect.y <= wall.y + wall.height)):
               print('left')
               self.colliding = True
               return 'left'

            elif ((self.rect.x - self.speed['speed_l'] >= wall.x + wall.width and self.rect.x <= wall.x + wall.width) and (self.rect.y + self.rect.height >= wall.y and self.rect.y <= wall.y + wall.height)):
               print('right')
               self.colliding = True
               return 'right'

            elif ((self.rect.y + self.rect.height - self.speed['speed_d'] <= wall.y and self.rect.y + self.rect.height >= wall.y) and (self.rect.x + self.rect.width >= wall.x and self.rect.x <= wall.x + wall.width)):
               print('bottom')
               self.colliding = True
               return 'bottom'

            elif ((self.rect.y - self.speed['speed_u'] >= wall.y + wall.height and self.rect.y <= wall.y + wall.height) and (self.rect.x + self.rect.width >= wall.x and self.rect.x <= wall.x + wall.width)):
               print('top')
               self.colliding = True
               return 'top'
            else:
                self.colliding = False

        return False


    def teleport(self):

        if (self.rect.x + self.rect.width <= 0):
            self.rect.x = screen_height

        elif (self.rect.x > screen_height):
            self.rect.x = -self.rect.width

        if (self.rect.y + self.rect.height <= 0):
            self.rect.y = screen_width

        elif (self.rect.y > screen_width):
            self.rect.y = -self.rect.height


    def check_nearby_wall(self, all_walls, dist = 2):
        '''
        check_wall_d = [self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + dist]
        check_wall_u = [self.rect.x + self.rect.width // 2, self.rect.y - dist]
        check_wall_r = [self.rect.x + self.rect.width + dist, self.rect.y + self.rect.height // 2]
        check_wall_l = [self.rect.x - dist, self.rect.y + self.rect.height // 2]

        direct = [False, False, False, False]

        for wall in all_walls:
            if (wall.collidepoint(check_wall_l)):
                direct[0] = True

            if (wall.collidepoint(check_wall_r)):
                direct[1] = True

            if (wall.collidepoint(check_wall_u)):
                direct[2] = True

            if (wall.collidepoint(check_wall_d)):
                direct[3] = True

        return direct
        '''

        direct = [False, False, False, False]

        cur_cell_i = self.get_loc_cell()[0]
        cur_cell_j = self.get_loc_cell()[1]

        if (all_walls[cur_cell_i][cur_cell_j - 1]):
            direct[0] = True
        if (all_walls[cur_cell_i][cur_cell_j + 1]):
            direct[1] = True
        if (all_walls[cur_cell_i - 1][cur_cell_j]):
            direct[2] = True
        if (all_walls[cur_cell_i + 1][cur_cell_j]):
            direct[3] = True

        print(direct)
        return direct

    def collision(self, *obj):

        list_of_all_object_groups = list(obj)
        # 0 - стены, 1 - семена, 2 - приведения, 3 - пакман
        # потом, может, сделаю чтобы распознавал в любом порядке *obj (нет)

        coll_wall = self.walls_collision(list_of_all_object_groups[0])
        
        self.teleport()

        #self.check_nearby_wall(list_of_all_object_groups[0])

        # ни че не тестил, чисто в теории
        self.mask = pygame.mask.from_surface(self.image)

        ghost_mas = list_of_all_object_groups[2].sprites()
        coll_ghost = []

        for ind in range(len(ghost_mas)):
            if (pygame.sprite.collide_mask(self, ghost_mas[ind])):
                coll_ghost.append(ind)


        #colcopac = list(pygame.sprite.collide_mask(list_of_all_object_groups[3], self))  # Координаты коллизии с пакманом
        #coll_pacman = [self.rect.x + colcopac[0], self.rect.y + colcopac[1]]

        status = [coll_wall, coll_ghost]
        #status = [coll_wall, coll_ghost, coll_pacman]

        return status


    def get_loc_cell(self):

        x = self.rect.x // cell_size
        y = self.rect.y // cell_size

        return [x, y]


    def draw(self, screen, x, y, s):

        self.rect.x = x
        self.rect.y = y
        self.conspeed = s
        self.last_loc_cell = self.get_loc_cell()