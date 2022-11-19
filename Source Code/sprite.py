import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction
        self.time = pygame.time.get_ticks()
        self.speed = 400

    def check_time(self):
        if((pygame.time.get_ticks() - self.time) / 1000 > 180):
            self.speed  = 700

    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x) , round(self.pos.y))
        self.check_time()