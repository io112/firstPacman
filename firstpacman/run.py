import sys
import pygame
from firstpacman.game import Game
import pathfinding


def main():
    pygame.init()
    pygame.font.init()
    game = Game()
    game.activity_manager()
    sys.exit()


if __name__ == '__main__':
    main()
