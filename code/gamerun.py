import pygame
from pygame.math import Vector2 as vector
import sys
from settings import *
from entity import Entity
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Cactus, Coffin
from gameover import gameOver
from sky import Sky


class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet, screen):
        super().__init__(pos, groups, path, collision_sprites)
        # Bullet
        self.create_bullet = create_bullet
        self.bullet_shot = False

        self.screen = screen

        self.health = 5

        self.death = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.bullet_shot = False

                match self.status.split('_')[0]:
                    case 'left': self.bullet_direction = vector(-1, 0)
                    case 'right': self.bullet_direction = vector(1, 0)
                    case 'up': self.bullet_direction = vector(0, -1)
                    case 'down': self.bullet_direction = vector(0, 1)

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:

            bullet_create_position = self.rect.center + self.bullet_direction * 80

            self.create_bullet(bullet_create_position, self.bullet_direction)
            self.bullet_shot = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def check_death(self):
        if self.health <= 0:
            self.death = 1

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.get_status()
        self.blink()

        self.hitted_timer()
        self.check_death()


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


class Gamerun():
    def __init__(self, screen, clock):
        pygame.init()
        self.display_surface = screen
        self.clock = clock
        self.bullets_surf = pygame.image.load(
            '../graphics/other/particle.png').convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        # Score
        self.score = 0

        # Death
        self.death = 0

        # Sky
        self.sky = Sky()

        self.setup()

    def score_update(self):
        # Score
        self.score = pygame.time.get_ticks() // 7000

    def check_gameOver(self):
        self.death = self.player.death
        if (self.death == 1):
            gameOver(self.display_surface, self.clock, self.score)

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
        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, [
                   self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet,
                    screen=self.display_surface)
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

        self.font = pygame.font.Font('../font/subatomic.ttf', 50)
        score_text = f'Score: {self.score}'
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
            self.all_sprites.customize_draw(self.player)

            # Score
            self.display_score()

            self.score_update()

            self.check_gameOver()

            # Day time
            self.sky.display(dt)

            pygame.display.update()
