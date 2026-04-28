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

        #Stats
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH

        #Tir
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # frames entre chaque tir

        #Invulnérabilité
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

        # Gérer le cooldown de tir
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, target_pos):
        if self.shoot_cooldown == 0:
            direction = pygame.math.Vector2(target_pos) - self.position
            projectile = Projectile(self.position.x, self.position.y, direction)
            self.shoot_cooldown = self.shoot_delay
            return projectile
        return None

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.velocity = direction.normalize() * 10

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position
        # Supprimer le projectile s'il sort de l'écran
        if not (0 <= self.position.x <= 1280 and 0 <= self.position.y <= 720):
            self.kill()