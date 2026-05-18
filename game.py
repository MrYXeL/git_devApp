import pygame
from ennemi import Ennemi
from player import Player
from slash import Slash
import pytmx
import pyscroll

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.running = True

        self.tmx_data = pytmx.util_pygame.load_pygame("assets/map.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2.5

        self.player_position = self.tmx_data.get_object_by_name("Player")
        self.player = Player(self.player_position.x, self.player_position.y)
        self.slash = None


        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.name == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "Ennemi":
                ennemi = Ennemi(obj.x, obj.y, target=self.player)
                self.group.add(ennemi)

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
                self.slash = slash_sprite

    def update(self):
        self.group.update()
        
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 and not isinstance(sprite, Slash):
                sprite.move_back()
            if isinstance(sprite, Ennemi) and self.slash and self.slash.active:
                if sprite.rect.colliderect(self.slash.rect):
                    sprite.get_hit()

    def death_screen(self):
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Game Over", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def victory_screen(self):
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("You Win!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def draw_hud(self):
        life_text = f"Vie:"
        for live in range(self.player.life):
            life_text += " O"
        enemies_remaining = sum(1 for s in self.group.sprites() if isinstance(s, Ennemi))
        enemy_text = f"Ennemis restants: {enemies_remaining}"

        life_surf = self.font.render(life_text, True, (255, 255, 255))
        enemy_surf = self.font.render(enemy_text, True, (255, 255, 255))

        bg_rect = life_surf.get_rect(topleft=(10, 10))
        bg_rect.width = max(bg_rect.width, enemy_surf.get_width())
        bg_rect.height = life_surf.get_height() + enemy_surf.get_height() + 10
        bg_rect.inflate_ip(10, 8)

        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        self.screen.blit(life_surf, (bg_rect.left + 5, bg_rect.top + 4))
        self.screen.blit(enemy_surf, (bg_rect.left + 5, bg_rect.top + 4 + life_surf.get_height()))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for sprite in self.group.sprites():
                if hasattr(sprite, "save_location"):
                    sprite.save_location()
            self.handle_input()
            self.update()
            
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.draw_hud()
            pygame.display.flip()

            if self.player.life <= 0:
                self.death_screen()
                self.running = False
            if not any(isinstance(s, Ennemi) for s in self.group.sprites()):
                self.victory_screen()
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            clock.tick(60) #FPS
        pygame.quit()