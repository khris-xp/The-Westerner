import pygame,sys


WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 620

PATHS = {
    'player': '../Infographic/graphics/player',
    'coffin': '../Infographic/graphics/monster/coffin',
    'cactus': '../Infographic/graphics/monster/cactus'
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))