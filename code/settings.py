import pygame,sys


WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 620

PATHS = {
    'player': '../graphics/player',
    'coffin': '../graphics/monster/coffin',
    'cactus': '../graphics/monster/cactus'
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))