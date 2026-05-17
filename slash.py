import pygame
import animation

class Slash(animation.AnimateSprite):
    OFFSET = {
        "left": (-10, 0),
        "right": (10, 0),
        "up": (0, -10),
        "down": (0, 10)
    }

    def __init__(self, player):
        super().__init__("player")
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.player = player
        self.position = player.position.copy()
        self.direction = player.direction
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.set_animation(f"slash_{self.direction}")
        # Force l'affichage de la première frame
        frames = self.images[self.current_animation]
        self.image = frames[self.current_image]

    def update(self):
        self.position = self.player.position.copy()
        offset_x, offset_y = self.OFFSET.get(self.direction, (0, 0))
        self.position[0] += offset_x
        self.position[1] += offset_y
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        frames = self.images[self.current_animation]
        old_index = self.current_image
        self.animate()
        if old_index == len(frames) - 1 and self.current_image == 0:
            self.kill()