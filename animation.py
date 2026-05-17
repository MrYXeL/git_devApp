import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f"assets/{sprite_name}/{sprite_name}.png")
        self.current_image = 0
        self.images = animation[sprite_name]
        self.current_animation = "idle_down"
        self.animation_speed = 8
        self.animation_frame = 0

    def set_animation(self, animation_name):
        if animation_name == self.current_animation:
            return
        self.current_animation = animation_name
        self.current_image = 0
        self.animation_frame = 0

    def animate(self):
        frames = self.images[self.current_animation]
        self.animation_frame += 1
        if self.animation_frame < self.animation_speed:
            return

        self.animation_frame = 0
        self.current_image += 1
        if self.current_image >= len(frames):
            self.current_image = 0
        self.image = frames[self.current_image]


def load_animation_images(sprite_name, animations, direction):
    images = []
    path = f"assets/{sprite_name}/{animations}/"

    for num in range(0, 8):
        image_path = path + f"{sprite_name}_{animations}_{direction}_{num}.png"
        images.append(pygame.image.load(image_path))
    return images

animation = {
    "player": {
        "idle_down": load_animation_images("player", "idle", "down"),
        "idle_up": load_animation_images("player", "idle", "up"),
        "idle_right": load_animation_images("player", "idle", "right"),
        "idle_left": load_animation_images("player", "idle", "left"),
        "run_down": load_animation_images("player", "run", "down"),
        "run_up": load_animation_images("player", "run", "up"),
        "run_right": load_animation_images("player", "run", "right"),
        "run_left": load_animation_images("player", "run", "left")
    }
}