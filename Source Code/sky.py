import pygame
from settings import *
import math
from random import randint


def signed(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.night = False
        self.start_color = [255, 255, 255]
        self.default_color = [255, 255, 255]
        self.end_color = [37, 100, 188]
        self.random_sky = randint(1, 5)

    def display(self):

        if ([math.ceil(x) for x in self.start_color] == [math.ceil(x) for x in self.end_color]):
            self.night = True
        if ([math.ceil(x) for x in self.start_color] == [math.ceil(x) for x in self.default_color]):
            self.night = False

        if (self.night == False):
            for i in range(3):
                if self.start_color[i] > self.end_color[i]:
                    self.start_color[i] -= (self.random_sky) / 100

        else:
            for i in range(3):
                if self.start_color[i] < self.default_color[i]:
                    self.start_color[i] += (self.random_sky) / 100

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(
            self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
