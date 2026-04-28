import pygame

PLAYER_COLOR = (50, 200, 50)
PLAYER_SPEED = 5
PLAYER_HEALTH = 5
INVULN_DURATION = 60  # Frames d'invulnérabilité après un dégât

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.invuln_frames = 0
        self.invuln_duration = INVULN_DURATION

    def update(self, keys):
        movement = pygame.math.Vector2(0, 0)
        if keys[pygame.K_q]:
            movement.x -= self.speed
        if keys[pygame.K_d]:
            movement.x += self.speed
        if keys[pygame.K_z]:
            movement.y -= self.speed
        if keys[pygame.K_s]:
            movement.y += self.speed

        self.position += movement
        self.rect.center = self.position

        # Gérer l'invulnérabilité
        if self.invuln_frames > 0:
            self.invuln_frames -= 1