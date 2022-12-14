import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin
from random import randint


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):

        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down_idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Based Movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        # Collisions
        self.hitbox = self.rect.inflate(-self.rect.width *
                                        0.4, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        self.mask = pygame.mask.from_surface(self.image)

        # Attack
        self.attacking = False

        self.damage_sound = pygame.mixer.Sound('../Infographic/sound/hit.mp3')

        # Health
        self.health = 3
        self.hitted = True
        self.hit_time = None

        # Critical
        self.critical = randint(0, 10)

    def blink(self):
        if not self.hitted:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def damage(self):
        self.critical = randint(0, 10)

        if self.hitted:
            self.damage_sound.play()
            self.health -= 1

            if (self.critical > 9):
                self.health -= 2

            self.hitted = False
            self.hit_time = pygame.time.get_ticks()  # Number in the millisecond

    def hitted_timer(self):
        if not self.hitted:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 400:
                self.hitted = True

    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def move(self, dt):

        # Another Angle Draw (normalize)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':  # horizontal
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
