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


class Game:
    def __init__(self):
        self.tanks = [Tank(init.WIDTH/2, init.HEIGHT/2, init.MAX_HEALTH, tank_img, barrel_img, bullet_img), Tank(init.WIDTH/2, init.HEIGHT/2, init.MAX_HEALTH, tank_img, barrel_img, bullet_img)]
        self.tank_sprites = pygame.sprite.Group()
        self.barrel_sprites = pygame.sprite.Group()
        self.bullets_sprites = pygame.sprite.Group()
        self.health_bars_sprites = pygame.sprite.Group()
        self.player_counter = -1

    def get_packages(self):
        return self.tank_sprites, self.barrel_sprites, self.health_bars_sprites, self.bullets_sprites

    def update(self, player_id, key_state):
            if key_state[pygame.K_LEFT]:
                self.tanks[player_id].turn_left()
            elif key_state[pygame.K_RIGHT]:
                self.tanks[player_id].turn_right()
            else:
                self.tanks[player_id].stop_moving()

            self.tank_sprites.update()
            self.tank_sprites.draw(screen)
            pygame.display.flip()

