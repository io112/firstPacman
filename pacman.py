import pygame


class Object(pygame.sprite.Sprite):

    def __init__(self, picture=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = picture
        if picture is not None:
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)


class Pacman(Object):

    def __init__(self):
        super().__init__(pygame.image.load("packman_circle.png"))
        self.hp = 3
        self.move_dir = ''
        self.prev_move_dir = 'none'
        self.change_sprite = 1
        self.is_moving = False
        self.open_havalka_timer = False
        self.cur_move_sprite = pygame.image.load("packman_circle.png")
        self.clock = pygame.time.Clock()
        self.time = 0

    def set_movement(self, direction, move_status):
        self.is_moving = move_status
        self.move_dir = direction

        if self.move_dir != self.prev_move_dir:
            self.prev_move_dir = self.move_dir
            print('change')
            self.time = 300

        if self.is_moving:
            self.open_havalka_timer = True
        else:
            self.open_havalka_timer = False

    def move(self):
        dirs = ['left', 'right', 'up', 'down']
        if self.is_moving:

            if self.move_dir == dirs[0]:
                self.rect.move_ip(-1, 0)
                self.cur_move_sprite = pygame.image.load("packman_left.png")
            elif self.move_dir == dirs[1]:
                self.rect.move_ip(1, 0)
                self.cur_move_sprite = pygame.image.load("packman_right.png")
            elif self.move_dir == dirs[2]:
                self.rect.move_ip(0, -1)
                self.cur_move_sprite = pygame.image.load("packman_top.png")
            elif self.move_dir == dirs[3]:
                self.rect.move_ip(0, 1)
                self.cur_move_sprite = pygame.image.load("packman_bottom.png")

    def collision(self, *args):
        all_objects = list(*args)
        print(all_objects)
        # Будет поле, будет и коллизия

    def change(self):
        if self.open_havalka_timer:
            self.time += self.clock.tick_busy_loop(60)
            print(self.time)
            if (self.time > 300):
                # print(self.change_sprite)

                if (self.change_sprite > 0):
                    self.image = pygame.image.load("packman_circle.png")
                    print('circle')

                elif (self.change_sprite < 0):
                    print('nope')
                    self.image = self.cur_move_sprite

                self.change_sprite *= -1
                self.time = 0


size = width, height = 800, 600
black = 0, 0, 0
color = 72, 61, 140


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    game_end = False

    # pacman_sprite = pygame.image.load("packman_circle.png")

    pacman = Pacman()
    pacman.rect.x = width // 2
    pacman.rect.y = height // 2
    player = pygame.sprite.Group()
    player.add(pacman)

    # wall = Object()
    # wall.rect = pygame.Rect([400, 300, 50, 50], color = (255, 255, 255), size = 1)

    while (not game_end):

        for event in pygame.event.get():

            if (event.type == pygame.KEYDOWN):

                if (event.key == pygame.K_RIGHT):
                    pacman.set_movement('right', True)
                elif (event.key == pygame.K_LEFT):
                    pacman.set_movement('left', True)
                elif (event.key == pygame.K_UP):
                    pacman.set_movement('up', True)
                elif (event.key == pygame.K_DOWN):
                    pacman.set_movement('down', True)

            if (event.type == pygame.QUIT):
                game_end = True

        if (pacman.is_moving):
            pacman.move()

        # pacman.collision()
        pacman.change()

        screen.fill(black)
        player.draw(screen)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
