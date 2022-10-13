import pygame
from sys import exit
from random import choice

shape = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx']


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/pngegg.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(400, 550))
        self.ready = True
        self.cooldown = 600

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= 8
        if keys[pygame.K_d] and self.rect.x < 730:
            self.rect.x += 8
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.cooldown:
                self.ready = True

    def shoot_laser(self):
        laser_group_player.add(Laser(self.rect.center, "player"))

    def update(self):
        self.move()
        self.recharge()
        laser_group_player.update()
        laser_group_alien.update()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, person):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.rect = self.image.get_rect(center=pos)
        self.image.fill("red")
        if person == "alien":
            self.speed = 8
        elif person == "player":
            self.speed = -8

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= 650:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()
        self.laser_time = None
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 1
        self.ready = True
        self.cooldown = 2000

    def update(self):
        self.rect.x += self.speed
        self.check()
        self.recharge()
        self.shoot()

    def check(self):
        all_aliens = alien_group.sprites()
        for alien in all_aliens:
            if alien.rect.right > WIDTH:
                self.speed = -1
                # self.move_down(1)
            if alien.rect.left < 0:
                self.speed = 1
                # self.move_down(1)

    def shoot(self):
        if self.ready:
            self.alien_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.cooldown:
                self.ready = True
                return True

    def move_down(self, distance):
        if alien_group:
            for alien in alien_group.sprites():
                alien.rect.y += distance

    def alien_laser(self):
        if alien_group:
            random_alien = choice(alien_group.sprites())
            laser_group_alien.add(Laser(random_alien.rect.center, "alien"))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("images/pngegg (4).png")
        self.rect = self.image.get_rect(midbottom=(x, 500))


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

LIVES = 3
live_surf = pygame.image.load("images/pngegg.png").convert_alpha()
live_x_start_pos = WIDTH - (live_surf.get_size()[0] * 2 + 20)
score = 0

background = pygame.image.load("images/backround.png")
screen.blit(background, (0, 0))
clock = pygame.time.Clock()

player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

laser = Laser(player.rect.center, "player")
laser_group_player = pygame.sprite.Group()
laser_group_alien = pygame.sprite.Group()

obstacle_group = pygame.sprite.Group()
for i in range(3):
    obstacle = Obstacle(150 + i * 250)
    obstacle_group.add(obstacle)


def Collision_Check():
    global score
    global LIVES
    for laser in laser_group_player.sprites():
        if pygame.sprite.spritecollide(laser, obstacle_group, False):
            laser.kill()
        if pygame.sprite.spritecollide(laser, alien_group, True):
            laser.kill()
            score += 100
            collision_sound.play()
    for laser in laser_group_alien.sprites():
        if pygame.sprite.spritecollide(laser, player_group, False):
            LIVES -= 1
            if LIVES <= 0:
                pygame.quit()
                exit()
        if pygame.sprite.spritecollide(laser, obstacle_group, False):
            laser.kill()


def display_lives():
    global LIVES
    for live in range(LIVES):
        x = live_x_start_pos + (live * live_surf.get_width()) + 15
        screen.blit(live_surf, (x, 550))


def display_score():
    font = pygame.font.SysFont("arial", 30, bold=True)
    score_surf = font.render(f"score: {score}", False, "white")
    score_rect = score_surf.get_rect(topleft=(0, 550))
    screen.blit(score_surf, score_rect)


def victory():
    if not alien_group.sprites():
        font = pygame.font.SysFont("arial", 30, bold=True)
        victory_surf = font.render('You won', False, 'white')
        victory_rect = victory_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(victory_surf, victory_rect)


alien_group = pygame.sprite.Group()
for i in range(7):
    alien = Aliens((200 + i * 65), 55, "images/pngegg (1).png")
    alien_group.add(alien)
for i in range(7):
    alien = Aliens((200 + i * 65), 110, "images/pngegg (2).png")
    alien_group.add(alien)
for i in range(7):
    alien = Aliens((200 + i * 65), 165, "images/pngegg (2).png")
    alien_group.add(alien)
for i in range(7):
    alien = Aliens((200 + i * 65), 220, "images/pngegg (3).png")
    alien_group.add(alien)

# obstacle_group = pygame.sprite.Group()
ALIENLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ALIENLASER, 800)

#
music_back = pygame.mixer.Sound("music/music.wav")
music_back.set_volume(0.2)
music_back.play(-1)
laser_sound = pygame.mixer.Sound("music/laser.wav")
laser_sound.set_volume(0.3)
collision_sound = pygame.mixer.Sound("music/explosion.wav")
collision_sound.set_volume(0.3)

while True:
    pygame.display.update()
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # if event.type == ALIENLASER:
        #     laser.update()

    player_group.draw(screen)
    laser_group_alien.draw(screen)
    laser_group_player.draw(screen)
    alien_group.draw(screen)
    obstacle_group.draw(screen)
    Collision_Check()
    alien_group.update()
    player_group.update()
    display_lives()
    display_score()
    victory()
    pygame.display.update()
    clock.tick(45)
