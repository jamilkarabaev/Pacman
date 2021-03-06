import pygame
import random
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
pygame.init()

size = (640, 800)
screen = pygame.display.set_mode(size)

sprites_group = pygame.sprite.Group()
pacman_group = pygame.sprite.Group()
ghosts_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
powerups_group = pygame.sprite.Group()
pacdots_group = pygame.sprite.Group()

pacman_image = pygame.image.load('pac-png.png')
cells = pygame.image.load('cells.png')
speed_power_up_image = pygame.image.load('speed_power_up.png')

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pacman_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100
        self.score = 0
        self.damage = 100
        self.score = 0

    def update(self):
        self.rect.x += self.speed_x
        self.collide_x(walls_group)
        self.rect.y += self.speed_y
        self.collide_y(walls_group)
        self.score_check()
        self.display_score()

    def collide_x(self, sprite_group):
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
        for block in block_hit_list:
            if self.speed_x > 0:
                self.rect.right = block.rect.left
            elif self.speed_x < 0:
                self.rect.left = block.rect.right

    def collide_y(self, sprite_group):
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
        for block in block_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            elif self.speed_y < 0:
                self.rect.top = block.rect.bottom

    def score_check(self):
        block_hit_list = pygame.sprite.spritecollide(self, pacdots_group, False)
        if block_hit_list:
            self.score += 1


    def display_score(self):
        font = pygame.font.SysFont("serif", 25)
        score = font.render("score: " + str(self.score), True, BLACK)
        screen.blit(score, [10, 650])
    


player = Pacman(40,40)
pacman_group.add(player)
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,40])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GhostCageWall(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image.fill(BLUE)

class CageDoor(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x ,y)
        self.image = cells

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,40])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.consumed = False
    

    def update(self):
        self.check_if_consumed(pacman_group)

    def check_if_consumed(self, sprite_group):
        block_hit_list = pygame.sprite.spritecollide(self, sprite_group, False)
        if block_hit_list:
            self.consumed = True
            self.kill()
            player.speed_x *= 2
            player.speed_y *= 2

class SpeedPowerUp(PowerUp):
    def __init__(self, x, y):
        PowerUp.__init__(self, x, y)
        self.image = speed_power_up_image


class PacDot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([8,8])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score_increment_value = 1

    def remove_on_pickup(self):
        block_hit_list = pygame.sprite.spritecollide(self, pacman_group, False)
        if block_hit_list:
            self.kill()

    def update(self):
        self.remove_on_pickup()

class Fruit(PacDot):
    def __init__(self, x, y):
        PacDot.__init__(self, x, y)
        self.image = pygame.Surface([30,30])
        self.image.fill(RED)
        self.score_increment_value = 10

fruit_sprite = Fruit(400,45)
pacdots_group.add(fruit_sprite)




sample_pac_dot = PacDot(200,60)
sample_pac_dot1 = PacDot(220,60)
sample_pac_dot2 = PacDot(260,60)
pacdots_group.add(sample_pac_dot)
pacdots_group.add(sample_pac_dot1)
pacdots_group.add(sample_pac_dot2)


speed_obj = SpeedPowerUp(40,80)
powerups_group.add(speed_obj)

        



Maps = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 2, 3, 3, 2, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 2, 0, 0, 2, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 2, 2, 2, 2, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

for y in range(len(Maps)):
    for x in range(len(Maps)+1):
        if Maps[y][x] == 1:
            wall = Wall(x*40, y*40)
            walls_group.add(wall)
        elif Maps[y][x] == 2:
            wall = GhostCageWall(x*40, y*40)
            walls_group.add(wall)
        elif Maps[y][x] == 3:
            wall = CageDoor(x*40, y*40)
            walls_group.add(wall)





done = False
clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_UP:
                player.speed_y = -5
            elif event.key == pygame.K_DOWN:
                player.speed_y = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.speed_y = 0
    
    screen.fill(WHITE)
    player.update()
    powerups_group.update()
    pacdots_group.update()
    sprites_group.draw(screen)
    walls_group.draw(screen)
    ghosts_group.draw(screen)
    powerups_group.draw(screen)
    pacman_group.draw(screen)  
    pacdots_group.draw(screen)





    pygame.display.flip()
    clock.tick(60)
pygame.quit()