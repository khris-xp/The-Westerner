import pygame
from settings import *


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 1 * (dt * 15)

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(
            self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
