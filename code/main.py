import pygame
from pygame.math import Vector2 as vector
import sys
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Cactus, Coffin

SCORE = 0

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('../graphics/other/bg.png').convert()

    def customize_draw(self, player):

        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        self.display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('The Westerner')
        self.clock = pygame.time.Clock()
        self.bullets_surf = pygame.image.load(
            '../graphics/other/particle.png').convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        self.setup()



    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullets_surf,
               [self.all_sprites, self.bullets])

    def bullet_collision(self):

        # Bullet obstacle collision
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True)

            # Bullet monster collision
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.monsters, False)

            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()

                # player bullet collision
        if pygame.sprite.spritecollide(self.player, self.bullets, True):
            self.player.damage()

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')

        # Tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

        # Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, [
                   self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet)
            if obj.name == 'Coffin':
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.monsters],
                    path=PATHS['coffin'],
                    collision_sprites=self.obstacles,
                    player=self.player
                )
            if obj.name == 'Cactus':
                Cactus(
                    pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.monsters],
                    path=PATHS['cactus'],
                    collision_sprites=self.obstacles,
                    player=self.player,
                    create_bullet=self.create_bullet
                )

    def display_score(self):
        
        global SCORE

        self.font = pygame.font.Font('../font/subatomic.ttf', 50)
        score_text = f'Score: {pygame.time.get_ticks() // 4000}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom=(
            WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            (255, 255, 255),
            text_rect.inflate(30, 30),
            width=8,
            border_radius=5
        )

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)
            self.bullet_collision()

            # draw groups
            self.display_surface.fill('black')
            self.all_sprites.customize_draw(self.player)

            # Score
            self.display_score()
            print(SCORE)

            pygame.display.update()
            


if __name__ == '__main__':
    game = Game()
    game.run()
