import pygame
from player import Player
import slash
import pytmx
import pyscroll

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        self.tmx_data = pytmx.util_pygame.load_pygame("assets/map.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2.5

        self.player_position = self.tmx_data.get_object_by_name("Player")
        self.player = Player(self.player_position.x, self.player_position.y)

        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.name == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        if pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.move_right()
        if not (pressed[pygame.K_z] or pressed[pygame.K_s] or pressed[pygame.K_q] or pressed[pygame.K_d]):
            self.player.idle()
        if pressed[pygame.K_SPACE]:
            slash_sprite = self.player.slash()
            if slash_sprite is not None:
                self.group.add(slash_sprite)

    def update(self):
        self.group.update()
        
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 and not isinstance(sprite, slash.Slash):
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            clock.tick(60) #FPS
        pygame.quit()