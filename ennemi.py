import pygame
import animation
import math


class Ennemi(animation.AnimateSprite):
    def __init__(self, x, y, target=None):
        super().__init__("ennemi")
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 0.8
        self.direction = "down"
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.target = target
        self.active = False
        self.life = 3
        self.hit_cooldown = 1000  # en millisecondes
        self.last_hit_time = 0

    def save_location(self):
        self.old_position = self.position.copy()

    def chase(self):
        if not self.target:
            return
        tx, ty = self.target.position
        dx = tx - self.position[0]
        dy = ty - self.position[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        nx = dx / dist
        ny = dy / dist
        self.position[0] += nx * self.speed
        self.position[1] += ny * self.speed

        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = "right"
                self.set_animation("run_right")
            else:
                self.direction = "left"
                self.set_animation("run_left")
        else:
            if dy > 0:
                self.direction = "down"
                self.set_animation("run_down")
            else:
                self.direction = "up"
                self.set_animation("run_up")
        if self.rect.colliderect(self.target.feet):
            self.target.get_hit()

    def get_hit(self):
        if pygame.time.get_ticks() - self.last_hit_time >= self.hit_cooldown:
            self.last_hit_time = pygame.time.get_ticks()
            self.life -= 1

    def update(self):
        if self.active:
            self.chase()
        else:
            tx, ty = self.target.position
            if abs(tx - self.position[0]) < 200 and abs(ty - self.position[1]) < 200:
                self.active = True
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.life <= 0:
            self.kill()
        self.animate()

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom