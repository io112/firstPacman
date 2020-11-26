import pygame

from entities.MovingObject import movingObject

class Pacman(movingObject):

    def __init__(self):
        super().__init__(pygame.image.load("images/pacman_circle.png"))

        self.type = 'pacman'
        self.hp = 3
        self.change_sprite = -1
        self.is_moving = False
        self.open_havalka_timer = False
        self.cur_move_sprite = pygame.image.load("images/pacman_circle.png")
        self.clock = pygame.time.Clock()
        self.time = 0

    def set_movement(self, move_status, direction = 'not change'):

        self.is_moving = move_status
        if (direction != 'not change'):
            self.move_dir = direction

        if (self.move_dir != self.prev_move_dir):
            self.prev_move_dir = self.move_dir
            #print('change')
            self.time = 300

        if (self.is_moving):
            self.open_havalka_timer = True
        else:
            self.open_havalka_timer = False



    def move(self):

        dirs = ['left', 'right', 'up', 'down']

        if (self.is_moving):

            if (self.move_dir == dirs[0]):

               self.rect.move_ip(self.speed['speed_l'], 0)
               self.cur_move_sprite = pygame.image.load("images/pacman_left.png")

            elif (self.move_dir == dirs[1]):

                self.rect.move_ip(self.speed['speed_r'], 0)
                self.cur_move_sprite = pygame.image.load("images/pacman_right.png")

            elif (self.move_dir == dirs[2]):

                self.rect.move_ip(0, self.speed['speed_u'])
                self.cur_move_sprite = pygame.image.load("images/pacman_top.png")

            elif (self.move_dir == dirs[3]):

                self.rect.move_ip(0, self.speed['speed_d'])
                self.cur_move_sprite = pygame.image.load("images/pacman_down.png")


    def logic(self, *all_obj):

        st = self.collision(*all_obj)
        list_of_all_object_groups = list(all_obj)

        #print(st[0])
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

        else:
            self.speed = {'speed_l': -self.conspeed, 'speed_r': self.conspeed, 'speed_u': -self.conspeed, 'speed_d': self.conspeed}



        # Просто ест семена всех типов, для начисление балов или эфектов будем проверять коллизию пакмана с семенем в классе семян.
        #pygame.sprite.spritecollide(self, list_of_all_object_groups[1], True)
        # на всякий случай
        self.mask = pygame.mask.from_surface(self.image)
        for seed in list_of_all_object_groups[1]:
            if (pygame.sprite.collide_mask(self, seed)):
                list_of_all_object_groups[1].remove(seed)



    def change(self):

        if (self.open_havalka_timer):
            self.time += self.clock.tick_busy_loop(60)
            #print(self.time)
            if (self.time > 300):
                #print(self.change_sprite)

                if (self.change_sprite > 0):
                    self.image = pygame.image.load("images/pacman_circle.png")
                    #print('circle')

                elif (self.change_sprite < 0):
                    #print('nope')
                    self.image = self.cur_move_sprite

                self.change_sprite *= -1
                self.time = 0


    def check_events(self, event):

        if (event.type == pygame.KEYDOWN):

            if (event.key == pygame.K_RIGHT):
                self.set_movement(True, 'right')

            elif (event.key == pygame.K_LEFT):
                self.set_movement(True, 'left')

            elif (event.key == pygame.K_UP):
                self.set_movement(True, 'up')

            elif (event.key == pygame.K_DOWN):
                self.set_movement(True, 'down')



    def update(self, *args, event):

        if(event != None):
            self.check_events(event)

        if (self.is_moving):
            self.move()

        self.change()
        self.logic(*args)
