import random


class Field:
    def __init__(self):
        self.FIELD_HEIGHT = 8
        self.FIELD_WEIGHT = 8
        self.BRANCH_COUNT = 4
        self.field = [[False for i in range(self.FIELD_HEIGHT)] for i in range(self.FIELD_WEIGHT)]

    def init_field(self):
        # шаг вниз (h) / вправо (w)
        # от (0; 0) до (FIELD_HEIGHT; FIELD_WEIGHT)
        h, w = 0, 0

        # генерация "путей"
        for _ in range(self.BRANCH_COUNT):
            for i in range(self.FIELD_HEIGHT):
                w += random.randint(0, 1)
                h += random.randint(0, 1)
                self.field[h][w] = True
            h, w = 0, 0

        # отзеркаливание от y
        for i in reversed(range(self.FIELD_HEIGHT)):
            for j in range(self.FIELD_WEIGHT):
                self.field[self.FIELD_HEIGHT - i][j] = self.field[i][j]

        # отзеркаливание от x
        for i in reversed(range(self.FIELD_HEIGHT)):
            for j in range(self.FIELD_WEIGHT):
                self.field[j][self.FIELD_WEIGHT - i] = self.field[j][i]

    def update(self):
        pass

    def draw(self):
        for i in range(self.FIELD_HEIGHT):
            for j in range(self.FIELD_WEIGHT):
                print(int(self.field[i][j]), end='')
            print('\n')
