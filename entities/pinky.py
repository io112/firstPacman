import pygame, random

from entities.MovingObject import movingObject
from constants import *

class Pinky(movingObject):

    def __init__(self, texture):
        super().__init__(texture)

        self.type = 'pinky'
        self.mode = 'collide'
        self.change_sprite = -1
        self.is_moving = False
        self.cur_move_sprite = texture
        self.change_mod_timer = True
        self.clock = pygame.time.Clock()
        self.time = 0

    def action(self, all_walls, dist = 1):

        is_nearby_walls = self.check_nearby_wall(all_walls, dist)
        free_dirs = [i for i in range(len(is_nearby_walls)) if (is_nearby_walls[i] == False)]

        # Функция рандомного выбора направления
        def rand_dir(free_dirs):
            new_rand_dir = random.randint(0, len(free_dirs))

            if (new_rand_dir == 0):
                new_rand_dir = 'left'

            elif (new_rand_dir == 1):
                new_rand_dir = 'right'

            elif (new_rand_dir == 2):
                new_rand_dir = 'up'

            elif (new_rand_dir == 3):
                new_rand_dir = 'down'

            return new_rand_dir
        #----------------------------------------


        dir = rand_dir(free_dirs)

        print(dir)
        self.set_movement(True, dir)
        self.set_speed(self.conspeed)
        self.mode = 'free'

        return



    def logic(self, *all_obj, field):

        st = self.collision(*all_obj)
        list_of_all_object_groups = list(all_obj)
        #print(self.get_loc_cell(list_of_all_object_groups[0]))
        #print(st[0])

        #print(self.get_loc_cell())

        if (st[0]):

            if (st[0] == 'left'):
                self.rect.move_ip(-self.conspeed, 0)
                self.speed['speed_r'] = 0
                #self.rect.x += 1

            elif (st[0] == 'right'):
                self.rect.move_ip(self.conspeed, 0)
                self.speed['speed_l'] = 0
                #self.rect.x -= 1

            elif (st[0] == 'top'):
                self.rect.move_ip(0, self.conspeed)
                self.speed['speed_u'] = 0
                #self.rect.y += 1

            elif (st[0] == 'bottom'):
                self.rect.move_ip(0, -self.conspeed)
                self.speed['speed_d'] = 0
                #self.rect.y -= 1



        if (self.last_loc_cell != self.get_loc_cell() and self.colliding):
            print('now')
            self.action(field.field)
            self.last_loc_cell = self.get_loc_cell()
        elif (pygame.time.get_ticks() % 50 == 0):
            print('now')
            self.action(field.field)
            self.last_loc_cell = self.get_loc_cell()



        for s in self.speed:
            if (not s):
                print('col')
                self.action(field.field)

        # print(is_nearby_walls)


    def change(self):

        if (self.change_mod_timer):
            self.time += self.clock.tick_busy_loop(60)
            #print(self.time)
            if (self.time > 1000):

                if (self.mode == 'collide'):
                    self.mode = 'free'
                else:
                    self.mode = 'collide'

                self.time = 0

    def update(self, field, *args):

        if (self.is_moving):
            self.move()

        #self.change()
        self.logic(*args, field=field)
