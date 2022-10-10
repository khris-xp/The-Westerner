import pygame , sys
from settings import *

class Game : 
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('The Westerner')
        self.clock = pygame.time.Clock()
    def run(self):
        while True : 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000 # dt in milliseconds
            pygame.display.update()

if __name__ == 'main' : 
    game = Game()
    game.run()