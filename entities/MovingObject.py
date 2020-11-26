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
               return 'left'

            elif ((self.rect.x - self.speed['speed_l'] >= wall.x + wall.width and self.rect.x <= wall.x + wall.width) and (self.rect.y + self.rect.height >= wall.y and self.rect.y <= wall.y + wall.height)):
               print('right')
               return 'right'

            elif ((self.rect.y + self.rect.height - self.speed['speed_d'] <= wall.y and self.rect.y + self.rect.height >= wall.y)and (self.rect.x + self.rect.width >= wall.x and self.rect.x <= wall.x + wall.width)):
               print('bottom')
               return 'bottom'

            elif ((self.rect.y - self.speed['speed_u'] >= wall.y + wall.height and self.rect.y <= wall.y + wall.height) and (self.rect.x + self.rect.width >= wall.x and self.rect.x <= wall.x + wall.width)):
               print('top')
               return 'top'

        return False


    def teleport(self, tp_zones = 0):

        if (self.rect.x + self.rect.width <= 0):
            self.rect.x = screen_height

        elif (self.rect.x > screen_height):
            self.rect.x = -self.rect.width

        if (self.rect.y + self.rect.height <= 0):
            self.rect.y = screen_width

        elif (self.rect.y > screen_width):
            self.rect.y = -self.rect.height

        # Пока не готово, обрабатывет телепортацию от вверхнего и нижнего края, т.к поле симметрично только по оси y
        # уже не нужно, но мало ли
        '''
        if ((self.rect.y >= screen_height) or (self.rect.y - self.rect.height <= 0)):
             
            randzone = 'none'
                
            for zone in tp_zones:
                
                if ((zone[0][0] <= self.rect.x <= zone[0][1] - self.rect.width):
                    
                    while (True):
                    
                        randzone = tp_zones[random.randint(0, len(tp_zones) - 1)]
                    
                        if (randzone[1] != self.rect.y):
                            
                            self.rect.x = randzone[0][0] + (self.rect.x - zone[0][0])
                            self.rect.y = randzone[1]
                            break          
        '''


    def collision(self, *obj):

        list_of_all_object_groups = list(obj)
        # 0 - стены, 1 - семена, 2 - приведения, 3 - пакман
        # потом, может, сделаю чтобы распознавал в любом порядке *obj (нет)

        coll_wall = self.walls_collision(list_of_all_object_groups[0])
        
        self.teleport()

        # ни че не тестил, чисто в теории
        '''
        ghost_mas = list_of_all_object_groups[3].sprites()
        coll_ghost = []

        for ind in range(len(ghost_mas)):
            if (pygame.sprite.collide_mask(self, ghost_mas[ind])):
                coll_ghost.append(ind)


        colcopac = list(pygame.sprite.collide_mask(list_of_all_object_groups[4], self))  # Координаты коллизии с пакманом
        coll_pacman = [self.rect.x + colcopac[0], self.rect.y + colcopac[1]]
        '''

        #status = [coll_wall, coll_ghost, coll_pacman]
        status = [coll_wall]

        return status


    def draw(self, screen, x, y, s):

        self.rect.x = x
        self.rect.y = y
        self.conspeed = s