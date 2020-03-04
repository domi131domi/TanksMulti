import pygame
import init
from network import Network


pygame.init()
screen = pygame.display.set_mode((init.WIDTH, init.HEIGHT))
pygame.display.set_caption("Tanks")
clock = pygame.time.Clock()

running = True
n = Network()
player_id = n.player_id
print("You are player", player_id)

tank_sprites = pygame.sprite.Group()
barrel_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
health_bars_sprites = pygame.sprite.Group()

while running:
    clock.tick(init.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key_state = pygame.key.get_pressed()

    tank_sprites, barrel_sprites, health_bars_sprites, bullets_sprites = n.send(key_state)
    screen.fill(init.DARK_GREY)
    tank_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
