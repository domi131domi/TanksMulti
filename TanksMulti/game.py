import pygame
import init
from os import path
from tank2 import Tank


pygame.init()
screen = pygame.display.set_mode((init.WIDTH, init.HEIGHT))
pygame.display.set_caption("Tanks")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'img')
tank_img = pygame.image.load(path.join(img_dir, "Tank.png")).convert()
tank_img = pygame.transform.rotate(tank_img, 270)
tank_img = pygame.transform.scale(tank_img, (init.TANK_WIDTH, init.TANK_HEIGHT))
barrel_img = pygame.image.load(path.join(img_dir, "GunTurret.png")).convert()
barrel_img = pygame.transform.rotate(barrel_img, 270)
barrel_img = pygame.transform.scale(barrel_img, (init.BARREL_WIDTH, init.BARREL_HEIGHT))
bullet_img = pygame.image.load(path.join(img_dir, "Bullet.png")).convert()
bullet_img = pygame.transform.rotate(bullet_img, 270)
bullet_img = pygame.transform.scale(bullet_img, (init.BULLET_WIDTH, init.BULLET_HEIGHT))


tank = Tank(init.WIDTH/2, init.HEIGHT/2, init.MAX_HEALTH, tank_img, barrel_img, bullet_img)

running = True
while running:
    clock.tick(init.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key_state = pygame.key.get_pressed()

    screen.fill(init.DARK_GREY)
    pygame.display.flip()

pygame.quit()
