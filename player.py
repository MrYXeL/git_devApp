import pygame
import animation
import slash

class Player(animation.AnimateSprite):
    def __init__(self, x, y):
        super().__init__("player")
        self.position = [x, y]
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.size = (16, 16)
        self.rect.topleft = self.position
        self.speed = 2
        self.direction = "down"
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.last_attack_time = 0
        self.attack_cooldown = 500  # en millisecondes
        self.life = 5
        self.hit_cooldown = 1000  # en millisecondes
        self.last_hit_time = 0
        self.sound_player_hurt = pygame.mixer.Sound("assets/sounds/player_hurt.mp3")
        self.sound_player_hurt.set_volume(0.05)

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        self.direction = "right"
        self.set_animation("run_right")

    def move_left(self):
        self.position[0] -= self.speed
        self.direction = "left"
        self.set_animation("run_left")

    def move_up(self):
        self.position[1] -= self.speed
        self.direction = "up"
        self.set_animation("run_up")
    
    def move_down(self):
        self.position[1] += self.speed
        self.direction = "down"
        self.set_animation("run_down")

    def idle(self):
        self.set_animation(f"idle_{self.direction}")

    def get_hit(self):
        if pygame.time.get_ticks() - self.last_hit_time >= self.hit_cooldown:
            self.last_hit_time = pygame.time.get_ticks()
            self.life -= 1
            self.sound_player_hurt.play()
            if self.life <= 0:
                print("Player is dead!")

    def slash(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            return slash.Slash(self)
        return None

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.animate()

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom