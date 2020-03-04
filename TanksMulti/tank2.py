import pygame
import init


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health):
        pygame.sprite.Sprite.__init__(self)
        self.max_health = max_health
        self.hp = max_health
        self.image = pygame.Surface((init.HEALTH_BAR_X * max_health, init.HEALTH_BAR_Y))
        self.image.fill(init.GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - init.HEALTH_ABOVE

    def update(self, x, y):
        self.image = pygame.transform.scale(self.image, (init.HEALTH_BAR_X * self.hp, init.HEALTH_BAR_Y))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - init.HEALTH_ABOVE

    def down(self, value):
        self.hp -= value
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        return self.hp == 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(image, rotation)
        self.rect = self.image.get_rect()
        self.rotation = rotation
        self.rect.center = (x, y)
        if rotation == 90 or rotation == 180:
            self.speed = -init.BULLET_SPEED
        else:
            self.speed = init.BULLET_SPEED

    def update(self, *args):
        if self.rotation == 0 or self.rotation == 180:
            self.rect.centerx += self.speed
        else:
            self.rect.centery += self.speed

        if self.rect.left > init.WIDTH or self.rect.right < 0 or self.rect.bottom > init.HEIGHT or self.rect.top < 0:
            self.kill()


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = image
        self.image_orig.set_colorkey(init.WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.canRotate = True
        self.rotation = 0
        self.direction = [1, 0]
        self.turningSpeed = 0
        self.tank_position = [x, y]

    def rotate(self):
        if self.turningSpeed != 0:
            self.rotation = (self.rotation + self.turningSpeed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = self.tank_position
            if self.rotation == 0:
                self.stop_turning()
                self.direction = [1, 0]
            elif self.rotation == 90:
                self.stop_turning()
                self.direction = [0, -1]
            elif self.rotation == 180:
                self.stop_turning()
                self.direction = [-1, 0]
            elif self.rotation == 270:
                self.stop_turning()
                self.direction = [0, 1]

    def stop_turning(self):
        self.turningSpeed = 0
        self.canRotate = True

    def turn_left(self):
        if self.canRotate:
            self.canRotate = False
            self.turningSpeed = init.TANK_TURNING_SPEED

    def turn_right(self):
        if self.canRotate:
            self.canRotate = False
            self.turningSpeed = -init.TANK_TURNING_SPEED

    def move(self):
        self.rect.center = self.tank_position

    def update(self, *args):
        self.move()
        self.rotate()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health, image_tank, image_barrel, image_bullet):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = image_tank
        self.image_orig.set_colorkey(init.BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.canMove = True
        self.canRotate = True
        self.speed = 0
        self.rotation = 0
        self.direction = [1, 0]
        self.turningSpeed = 0
        self.barrel = Barrel(x, y, image_barrel)
        self.bullet_image = image_bullet
        self.canShoot = True
        self.lastShot = 0
        self.health = HealthBar(self.rect.centerx, self.rect.centery, max_health)

    def move_forward(self):
        self.speed = init.TANK_SPEED

    def move_back(self):
        self.speed = -init.TANK_SPEED_B

    def stop_moving(self):
        self.speed = 0

    def stop_turning(self):
        self.turningSpeed = 0
        self.canMove = True
        self.canRotate = True

    def turn_left(self):
        if self.canRotate:
            self.canMove = False
            self.canRotate = False
            self.turningSpeed = init.TANK_TURNING_SPEED
            self.barrel.turn_left()

    def turn_right(self):
        if self.canRotate:
            self.canMove = False
            self.canRotate = False
            self.turningSpeed = -init.TANK_TURNING_SPEED
            self.barrel.turn_right()

    def get_barrel(self):
        return self.barrel

    def rotate(self):
        if self.turningSpeed != 0:
            self.rotation = (self.rotation + self.turningSpeed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            if self.rotation == 0:
                self.stop_turning()
                self.direction = [1, 0]
            elif self.rotation == 90:
                self.stop_turning()
                self.direction = [0, -1]
            elif self.rotation == 180:
                self.stop_turning()
                self.direction = [-1, 0]
            elif self.rotation == 270:
                self.stop_turning()
                self.direction = [0, 1]

    def move(self):
        if self.canMove:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            self.barrel.tank_position = self.rect.center

    def reload(self):
        if pygame.time.get_ticks() - self.lastShot > init.TANK_RELOAD_TIME:
            self.canShoot = True

    def update(self, *args):
        self.rotate()
        self.move()
        self.reload()
        self.health.update(self.rect.centerx, self.rect.centery)

    def get_health_bar(self):
        return self.health

    def turn_barrel_left(self):
        self.barrel.turn_left()

    def turn_barrel_right(self):
        self.barrel.turn_right()

    def fire(self):
        if self.canShoot and self.barrel.canRotate:
            self.lastShot = pygame.time.get_ticks()
            self.canShoot = False
            return Bullet(self.rect.centerx, self.rect.centery, self.barrel.rotation, self.bullet_image)
        else:
            return None

    def got_hit(self):
        self.health.down(init.BULLET_DMG)
        if self.health.is_dead():
            self.die()

    def die(self):
        self.health.kill()
        self.barrel.kill()
        self.kill()
