import pygame

DEBUG_MODE = False
VELOCITY_SCALE = 16
VELOCITY_COLOR = (20, 255, 20)
HITBOX_COLOR = (255, 20, 20)

class Debuger():
    def __init__(self):
        self.rect_queue = []
        self.line_queue = []
        self.curved_line_queue = []

    def draw_rect(self, rect, clr=HITBOX_COLOR):
        self.rect_queue.append((rect, clr))

    def draw_line(self, start_pos, end_pos, clr=VELOCITY_COLOR):
        self.line_queue.append((start_pos, end_pos, clr))

    def draw_curved_line(self, points, clr=VELOCITY_COLOR):
        self.curved_line_queue.append((points, clr))

    def draw(self, screen):
        if not DEBUG_MODE:
            self.rect_queue = []
            self.line_queue = []
            self.curved_line_queue = []
            return

        for rect in self.rect_queue:
            pygame.draw.rect(screen, rect[1], rect[0], 2)

        for line in self.line_queue:
            pygame.draw.line(screen, line[2], line[0], line[1], 2)

        for curved_line in self.curved_line_queue:
            pygame.draw.lines(screen, curved_line[1], False, curved_line[0], 2)

        self.rect_queue = []
        self.line_queue = []
        self.curved_line_queue = []

debuger = None