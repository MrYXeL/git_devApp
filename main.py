import pygame
from player import Player

#Init
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#Groupe de sprites
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

#Joueur
player = Player(640, 360)
all_sprites.add(player)


#Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    projectile = None
    if keys[pygame.K_UP]:
        #shoot vers haut
        projectile = player.shoot((player.position.x, player.position.y - 1))
    elif keys[pygame.K_DOWN]:
        #shoot vers bas
        projectile = player.shoot((player.position.x, player.position.y + 1))
    elif keys[pygame.K_LEFT]:
        #shoot vers gauche
        projectile = player.shoot((player.position.x - 1, player.position.y))
    elif keys[pygame.K_RIGHT]:
        #shoot vers droite
        projectile = player.shoot((player.position.x + 1, player.position.y))
    
    if projectile:
        all_sprites.add(projectile)
        projectiles.add(projectile)

    player.update(keys)
    for projectile in projectiles:
        projectile.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()