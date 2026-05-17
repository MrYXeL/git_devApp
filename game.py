import pygame
from player import Player
import player

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        #Groupe de sprites
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        #Joueur
        self.player = Player(640, 360)
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            keys = pygame.key.get_pressed()
            projectile = None
            if keys[pygame.K_UP]:
                #shoot vers haut
                projectile = self.player.shoot((self.player.position.x, self.player.position.y - 1))
            elif keys[pygame.K_DOWN]:
                #shoot vers bas
                projectile = self.player.shoot((self.player.position.x, self.player.position.y + 1))
            elif keys[pygame.K_LEFT]:
                #shoot vers gauche
                projectile = self.player.shoot((self.player.position.x - 1, self.player.position.y))   
            elif keys[pygame.K_RIGHT]:
                #shoot vers droite
                projectile = self.player.shoot((self.player.position.x + 1, self.player.position.y))
            
            if projectile:
                self.all_sprites.add(projectile)
                self.projectiles.add(projectile)

            self.player.update(keys)
            for projectile in self.projectiles:
                projectile.update()

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()