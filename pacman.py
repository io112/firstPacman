import pygame

class Object(pygame.sprite.Sprite):

    def __init__(self, picture = None):

        pygame.sprite.Sprite.__init__(self)
        self.image = picture
        if (picture != None):
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)


class Pacman(Object):

    def __init__(self):
        super().__init__(pygame.image.load("images/packman_circle.png"))
        self.hp = 3
        self.move_dir = ''
        self.prev_move_dir = 'none'
        self.change_sprite = -1
        self.is_moving = False
        self.open_havalka_timer = False
        self.cur_move_sprite = pygame.image.load("images/packman_circle.png")
        self.clock = pygame.time.Clock()
        self.time = 0

    def set_movement(self, direction, move_status):
        self.is_moving = move_status
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
                self.rect.move_ip(-1, 0)
                self.cur_move_sprite = pygame.image.load("images/packman_left.png")
            elif (self.move_dir == dirs[1]):
                self.rect.move_ip(1, 0)
                self.cur_move_sprite = pygame.image.load("images/packman_right.png")
            elif (self.move_dir == dirs[2]):
                self.rect.move_ip(0, -1)
                self.cur_move_sprite = pygame.image.load("images/packman_top.png")
            elif (self.move_dir == dirs[3]):
                self.rect.move_ip(0, 1)
                self.cur_move_sprite = pygame.image.load("images/packman_bottom.png")



    def collision(self, *args):
        pass
        # Будет поле, будет и коллизия


    def change(self):
        if (self.open_havalka_timer):
            self.time += self.clock.tick_busy_loop(60)
            #print(self.time)
            if (self.time > 300):
                #print(self.change_sprite)

                if (self.change_sprite > 0):
                    self.image = pygame.image.load("images/packman_circle.png")
                    #print('circle')

                elif (self.change_sprite < 0):
                    #print('nope')
                    self.image = self.cur_move_sprite

                self.change_sprite *= -1
                self.time = 0


    def check_events(self, event):
        if (event.type == pygame.KEYDOWN):

            if (event.key == pygame.K_RIGHT):
                self.set_movement('right', True)
            elif (event.key == pygame.K_LEFT):
                self.set_movement('left', True)
            elif (event.key == pygame.K_UP):
                self.set_movement('up', True)
            elif (event.key == pygame.K_DOWN):
                self.set_movement('down', True)


    def draw(self, screen):
        self.rect.x = width // 2 - self.rect.width
        self.rect.y = height // 2 - self.rect.height


    def update(self, event = None):

        if(event != None):
            self.check_events(event)

        if (self.is_moving):
            self.move()

        # pacman.collision()
        self.change()



# просто для теста
size = width, height = 800, 600
black = 0, 0, 0


def main():

    pygame.init()
    screen = pygame.display.set_mode(size)

    game_end = False

    pacman = Pacman()

    # Хз как это в класс закинуть, пока придется в main'е прописывать
    player = pygame.sprite.Group()
    player.add(pacman)
    #----

    pacman.draw(screen)

    while (not game_end):

        for event in pygame.event.get():

            pacman.update(event)

            if (event.type == pygame.QUIT):
                game_end = True

        pacman.update()  # Да, вызывать update дважды выглядит убого, но пока так...

        screen.fill(black)
        player.draw(screen)  # Хз как это в класс закинуть, пока придется в main'е прописывать
        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == '__main__':
    main()