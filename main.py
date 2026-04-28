import pygame
from player import Player

#Init
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#Groupe de sprites
all_sprites = pygame.sprite.Group()

#Joueur
player = Player(640, 360)
all_sprites.add(player)

#Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()