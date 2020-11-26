import random, pygame, pygame.locals
from scenes.walls import *
from pygame import Rect




class Field:
    def __init__(self):
        self.FIELD_HEIGHT = 36  # ACTUALLY WIDTH 36
        self.FIELD_WIDTH = 26   # ACTUALLY HEIGHT 26
        self.CELL_SIZE = 8
        self.CELL_SCALE = 4
        self.CELL_ACTUAL_SIZE = self.CELL_SIZE * self.CELL_SCALE
        self.tileset_image = pygame.image.load("images/tileset.png").convert()
        self.tileset_rect = self.tileset_image.get_rect()

        self.tile_table = []
        for tile_x in range(0, round(self.tileset_rect.width / self.CELL_SIZE)):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, round(self.tileset_rect.height / self.CELL_SIZE)):
                rect = (tile_x * self.CELL_SIZE, tile_y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                line.append(self.tileset_image.subsurface(rect))

        self.field = []

    def init_field(self):
        raw_field = gen_new_map(self.FIELD_HEIGHT, self.FIELD_WIDTH)

        surrounded_field = []
        for y in range(len(raw_field)):
            arr = []
            for x in range(len(raw_field[y])):
                arr.append(raw_field[y][x])
            surrounded_field += [arr]

        for x in range(0, self.FIELD_WIDTH):
            surrounded_field[x][0] = False
            surrounded_field[x][self.FIELD_HEIGHT - 1] = False

        for x in range(0, self.FIELD_WIDTH):
            surrounded_field[x][1] = surrounded_field[x][2]
            surrounded_field[x][self.FIELD_HEIGHT - 2] = surrounded_field[x][self.FIELD_HEIGHT - 3]

        for y in range(0, self.FIELD_HEIGHT):
            surrounded_field[0][y] = False
            surrounded_field[self.FIELD_WIDTH - 1][y] = False

        for y in range(0, self.FIELD_HEIGHT):
            surrounded_field[1][y] = surrounded_field[2][y]
            surrounded_field[self.FIELD_WIDTH - 2][y] = surrounded_field[self.FIELD_WIDTH - 3][y]

        rotated_field = list(zip(*surrounded_field[::-1]))  # Rotated Matrix
        self.field = rotated_field

        self.FIELD_WIDTH = len(self.field[0]) - 2
        self.FIELD_HEIGHT = len(self.field) - 2

        # for i in range(len(self.field)):
        #     print(self.field[i])

    def update(self):
        pass

    def get_tile_world_coords(self, x, y):
        return [(x - 2) * self.CELL_ACTUAL_SIZE, (y - 2) * self.CELL_ACTUAL_SIZE]

    def check_tile(self, x, y):
        if self.field[int((x + 2) / self.CELL_ACTUAL_SIZE)][int((y + 2) / self.CELL_ACTUAL_SIZE)]:
            return True
        else:
            return False

    def get_all_wall_rects(self):
        rects = []
        for x in range(self.FIELD_HEIGHT + 1):
            for y in range(self.FIELD_WIDTH + 1):
                if self.field[x][y]:
                    rects.append(Rect((x - 2) * self.CELL_ACTUAL_SIZE, (y - 2) * self.CELL_ACTUAL_SIZE, self.CELL_ACTUAL_SIZE, self.CELL_ACTUAL_SIZE))
        return rects

    def draw(self, screen):
        for x in range(0, self.FIELD_HEIGHT):
            for y in range(0, self.FIELD_WIDTH):
                if (self.field[x][y]): # Координаты на 1 больше, потому что само поле вокруг состоит из 0. Так удобнее при расчетах
                    pos_x = (x - 2) * self.CELL_ACTUAL_SIZE # Координаты квадратика
                    pos_y = (y - 2) * self.CELL_ACTUAL_SIZE

                    texture = self.get_tile(x, y)
                    texture = pygame.transform.scale(texture, (self.CELL_ACTUAL_SIZE, self.CELL_ACTUAL_SIZE))
                    screen.blit(texture, (pos_x, pos_y, self.CELL_ACTUAL_SIZE, self.CELL_ACTUAL_SIZE))

        # self.draw_hitboxes(screen)

    def draw_hitboxes(self, screen):
        rects = self.get_all_wall_rects()
        for rect in rects:
            pygame.draw.rect(screen, (255, 0, 0), rect, 1)

    def get_tile(self, x, y):

        # #0#
        # 011
        # #11
        if (True and (not self.field[x][y - 1]) and True and
                (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[0][0]

        # #0#
        # 111
        # 111
        if (True and not (self.field[x][y - 1]) and True and
             (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[1][0]

        # #0#
        # 110
        # 11#
        if (True and (not self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[2][0]

        # #11
        # 011
        # #11
        if (True and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              True and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[0][1]

        # 111
        # 111
        # 111
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
             (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[1][1]

        # 11#
        # 110
        # 11#
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
             (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[2][1]

        # #11
        # 011
        # #0#
        if (True and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[0][2]

        # 111
        # 111
        # #0#
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
             (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[1][2]

        # 11#
        # 110
        # #0#
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
             (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[2][2]

        # #0#
        # 011
        # #0#
        if (True and (not self.field[x][y - 1]) and True and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[0][3]

        # #0#
        # 111
        # #0#
        if (True and (not self.field[x][y - 1]) and True and
             (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[1][3]

        # #0#
        # 110
        # #0#
        if (True and (not self.field[x][y - 1]) and True and
             (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[2][3]

        # #0#
        # 010
        # #1#
        if (True and (not self.field[x][y - 1]) and True and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              True and (self.field[x][y + 1]) and True):
            return self.tile_table[3][0]

        # #1#
        # 010
        # #1#
        if (True and (self.field[x][y - 1]) and True and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              True and (self.field[x][y + 1]) and True):
            return self.tile_table[3][1]

        # #1#
        # 010
        # #0#
        if (True and (self.field[x][y - 1]) and True and
             (not self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
              True and (not self.field[x][y + 1]) and True):
            return self.tile_table[3][2]

        # #0#
        # 010
        # #0#
        if (True and (not self.field[x][y - 1]) and True and
            (not self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
            True and (not self.field[x][y + 1]) and True):
            return self.tile_table[3][3]

        # #0#
        # 011
        # #10
        if (True and (not self.field[x][y - 1]) and True and
            (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
            True and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[4][0]

        # #0#
        # 111
        # 110
        if (True and (not self.field[x][y - 1]) and True and
            (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
            (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[5][0]

        # #0#
        # 111
        # 011
        if (True and (not self.field[x][y - 1]) and True and
            (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
            (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[6][0]

        # #0#
        # 110
        # 01#
        if (True and (not self.field[x][y - 1]) and True and
            (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
            (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[7][0]


        # #11
        # 011
        # #10
        if (True and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[4][1]

        # 111
        # 111
        # 110
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
            (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
            (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[5][1]

        # 111
        # 111
        # 011
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[6][1]

        # 11#
        # 110
        # 01#
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[7][1]

        # #10
        # 011
        # #11
        if (True and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[4][2]

        # 110
        # 111
        # 111
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[5][2]

        # 011
        # 111
        # 111
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[6][2]

        # 01#
        # 110
        # 11#
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[7][2]

        # #10
        # 011
        # #0#
        if (True and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (not self.field[x][y + 1]) and True):
            return self.tile_table[4][3]

        # 110
        # 111
        # #0#
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (not self.field[x][y + 1]) and True):
            return self.tile_table[5][3]

        # 011
        # 111
        # #0#
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (not self.field[x][y + 1]) and True):
            return self.tile_table[6][3]

        # 01#
        # 110
        # #0#
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
                True and (not self.field[x][y + 1]) and True):
            return self.tile_table[7][3]

        # #10
        # 011
        # #10
        if (True and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (not self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[4][4]

        # 110
        # 111
        # 110
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[5][4]

        # 011
        # 111
        # 011
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[6][4]

        # 01#
        # 110
        # 01#
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (not self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and True):
            return self.tile_table[7][4]

        # #0#
        # 111
        # 010
        if (True and (not self.field[x][y - 1]) and True and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[8][0]

        # 111
        # 111
        # 010
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[8][1]

        # 010
        # 111
        # 111
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[8][2]

        # 010
        # 111
        # #0#
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                True and (not self.field[x][y + 1]) and True):
            return self.tile_table[8][3]

        # 010
        # 111
        # 010
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[8][5]

        # 110
        # 111
        # 011
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[9][0]

        # 011
        # 111
        # 110
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[9][1]

        # 010
        # 111
        # 011
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
            (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (self.field[x + 1][y + 1])):
            return self.tile_table[9][2]

        # 011
        # 111
        # 010
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[9][3]

        # 010
        # 111
        # 110
        if ((not self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[10][2]

        # 110
        # 111
        # 010
        if ((self.field[x - 1][y - 1]) and (self.field[x][y - 1]) and (not self.field[x + 1][y - 1]) and
                (self.field[x - 1][y]) and (self.field[x][y]) and (self.field[x + 1][y]) and
                (not self.field[x - 1][y + 1]) and (self.field[x][y + 1]) and (not self.field[x + 1][y + 1])):
            return self.tile_table[10][3]

        return self.tile_table[10][4]

