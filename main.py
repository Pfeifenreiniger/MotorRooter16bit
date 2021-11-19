'''
16 bit pixelart version of the glorious Mario Party 3 minigame Motor Rooter
(with some game mechanic changes & enhancements of those)
Code by Kevin Spathmann
Graphics by Nintendo & Kevin Spathmann
Fonts used: "Mario Kart DS" by David (https://www.dafont.com/mario-kart-ds.font)
            "Super Mario 64 DS" by David (https://www.dafont.com/super-mario-64-ds.font)
            "Press Start 2P" by codeman38 (https://www.fontspace.com/press-start-2p-font-f11591)
Music used: "We Are Number One 16 Bit Remix" by RockstarTylerK
            "Nice and Easy (Mario Party 3)" by Nintendo
Original Game (included in Mario Party 3) by Nintendo
'''

import pygame, sys, random
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Motor Rooter 16 Bit Remix")
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("font/PressStart2P-vaV7.ttf", 20)
marioKart_font = pygame.font.Font("font/Mario-Kart-DS.ttf", 40)
mario64_font = pygame.font.Font("font/Super-Mario-64-DS.ttf", 20)
title_music = pygame.mixer.Sound("music/RockstarTylerK - We Are Number One 16Bit Remix.mp3")
title_music.set_volume(0.5)
title_music_played = False
game_music = pygame.mixer.Sound("music/Nintendo - Nice and Easy (Mario Party 3).mp3")
game_music.set_volume(0.5)
car_sfx = pygame.mixer.Sound("music/space_ship_floating_sound_1.mp3")
car_sfx.set_volume(0.4)
hit_sfx = pygame.mixer.Sound("music/Whoosh_Electric_02.wav")

### Spieler ###
class Player:
    def __init__(self):
        self.imgs = [pygame.image.load("graphics/player/player_6uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_7uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_9uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_11uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_12uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_1uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_3uhr.png").convert_alpha(), pygame.image.load("graphics/player/player_5uhr.png").convert_alpha()]
        self.life = 6
        self.x = 350    ## Startposition x 350
        self.y = 380    ## startposition y 380
        self.speed = 12
        self.rect = self.imgs[0].get_rect(topleft=(self.x, self.y))
        self.collision_immune = False
        self.collision_time = 0

    def player_input(self):
        global playerframe
        keys = pygame.key.get_pressed()
        ## 6 Uhr
        if keys[pygame.K_LEFT] and self.rect.left >= 200 and self.rect.top >= 380:
            if self.rect.left - self.speed <= 200:
                self.rect.left = 199
                self.rect.top = 379
                playerframe = 1
            else:
                playerframe = 0
                self.rect.left -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left <= 490 and self.rect.top >= 380:
            if self.speed + self.rect.left >= 490:
                self.rect.left = 491
                self.rect.top = 379
                playerframe = 7
            else:
                playerframe = 0
                self.rect.right += self.speed
        ## 7 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left <= 200 and self.rect.left >= 110 and self.rect.top >= 300:
            if self.rect.left - self.speed <= 100 or self.rect.top - self.speed <= 300:
                self.rect.left = 109
                self.rect.top = 299
                playerframe = 2
            else:
                playerframe = 1
                self.rect.left -= self.speed
                self.rect.top -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left <= 200 and self.rect.top <= 380 and self.rect.top >= 300:
            if self.rect.left + self.speed >= 220 or self.rect.top + self.speed >= 380:
                self.rect.left = 201
                self.rect.top = 381
                playerframe = 0
            else:
                playerframe = 1
                self.rect.left += self.speed
                self.rect.top += self.speed
        ## 9 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left <= 110 and self.rect.top >= 100:
            if self.rect.top - self.speed <= 100:
                self.rect.left = 111
                self.rect.top = 99
                playerframe = 3
            else:
                playerframe = 2
                self.rect.top -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left <= 110 and self.rect.top <= 300:
            if self.rect.top + self.speed >= 300:
                self.rect.left = 111
                self.rect.top = 301
                playerframe = 1
            else:
                playerframe = 2
                self.rect.top += self.speed
        ## 11 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left <= 220 and self.rect.top >= 10 and self.rect.top <= 100:
            if self.rect.left + self.speed >= 220 or self.rect.top - self.speed <= 10:
                self.rect.left = 221
                self.rect.top = 9
                playerframe = 4
            else:
                playerframe = 3
                self.rect.top -= self.speed
                self.rect.left += self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left <= 220 and self.rect.top <= 100:
            if self.rect.left - self.speed <= 110 or self.rect.top + self.speed >= 100:
                self.rect.left = 109
                self.rect.top = 101
                playerframe = 2
            else:
                playerframe = 3
                self.rect.top += self.speed
                self.rect.left -= self.speed
        ## 12 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left >= 220 and self.rect.left <= 510 and self.rect.top <= 10:
            if self.rect.left + self.speed >= 510:
                self.rect.left = 511
                self.rect.top = 11
            else:
                playerframe = 4
                self.rect.left += self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left >= 220 and self.rect.top <= 10:
            if self.rect.left - self.speed <= 220:
                self.rect.left = 219
                playerframe = 3
            else:
                playerframe = 4
                self.rect.left -= self.speed
        ## 1 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left >= 510 and self.rect.top >= 10 and self.rect.top <= 100:
            if self.rect.left + self.speed >= 560 or self.rect.top + self.speed >= 100:
                self.rect.left = 561
                self.rect.top = 101
            else:
                playerframe = 5
                self.rect.top += self.speed
                self.rect.left += self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left >= 510 and self.rect.top >= 10 and self.rect.top <= 100:
            if self.rect.left - self.speed <= 510 or self.rect.top - self.speed <= 10:
                self.rect.left = 509
                self.rect.top = 10
            else:
                playerframe = 5
                self.rect.top -= self.speed
                self.rect.left -= self.speed
        ## 3 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left >= 560 and self.rect.top >= 100 and self.rect.top <= 320:
            if self.rect.top + self.speed >= 320:
                self.rect.top = 321
                self.rect.left = 559
            else:
                playerframe = 6
                self.rect.top += self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left >= 560 and self.rect.top <= 320 and self.rect.top >= 100:
            if self.rect.top - self.speed <= 100:
                self.rect.top = 99
                self.rect.left = 559
            else:
                playerframe = 6
                self.rect.top -= self.speed
        ## 5 Uhr
        elif keys[pygame.K_LEFT] and self.rect.left >= 490 and self.rect.top >= 320 and self.rect.top <= 380:
            if self.rect.left - self.speed <= 490 or self.rect.top + self.speed >= 380:
                self.rect.left = 489
                self.rect.top = 381
            else:
                playerframe = 7
                self.rect.left -= self.speed
                self.rect.top += self.speed
        elif keys[pygame.K_RIGHT] and self.rect.left >= 490 and self.rect.top <= 380 and self.rect.top >= 320:
            if self.rect.left + self.speed >= 560 or self.rect.top - self.speed <= 320:
                self.rect.left = 561
                self.rect.top = 319
            else:
                playerframe = 7
                self.rect.left += self.speed
                self.rect.top -= self.speed
    def inv_frames(self):
        inv_model = self.imgs[playerframe].copy()
        inv_model.set_alpha(128)
        screen.blit(inv_model, self.rect)
    def draw_life(self):
        heart1_surf = pygame.image.load("graphics/player/life_counter/full_life.png").convert_alpha()
        heart2_surf = pygame.image.load("graphics/player/life_counter/full_life.png").convert_alpha()
        heart3_surf = pygame.image.load("graphics/player/life_counter/full_life.png").convert_alpha()
        if self.life == 6:
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            heart2_rect = heart2_surf.get_rect(topleft=(81, 10))
            heart3_rect = heart3_surf.get_rect(topleft=(137, 10))
            screen.blit(heart1_surf, heart1_rect)
            screen.blit(heart2_surf, heart2_rect)
            screen.blit(heart3_surf, heart3_rect)
        elif self.life == 5:
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            heart2_rect = heart2_surf.get_rect(topleft=(81, 10))
            heart3_surf = pygame.image.load("graphics/player/life_counter/half_life.png").convert_alpha()
            heart3_rect = heart3_surf.get_rect(topleft=(137, 10))
            screen.blit(heart1_surf, heart1_rect)
            screen.blit(heart2_surf, heart2_rect)
            screen.blit(heart3_surf, heart3_rect)
        elif self.life == 4:
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            heart2_rect = heart2_surf.get_rect(topleft=(81, 10))
            screen.blit(heart1_surf, heart1_rect)
            screen.blit(heart2_surf, heart2_rect)
        elif self.life == 3:
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            heart2_surf = pygame.image.load("graphics/player/life_counter/half_life.png").convert_alpha()
            heart2_rect = heart2_surf.get_rect(topleft=(81, 10))
            screen.blit(heart1_surf, heart1_rect)
            screen.blit(heart2_surf, heart2_rect)
        elif self.life == 2:
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            screen.blit(heart1_surf, heart1_rect)
        elif self.life == 1:
            heart1_surf = pygame.image.load("graphics/player/life_counter/half_life.png").convert_alpha()
            heart1_rect = heart1_surf.get_rect(topleft=(25, 10))
            screen.blit(heart1_surf, heart1_rect)
player = Player()

def player_reset():
    global playerframe
    player.speed = 12
    player.collision_immune = False
    player.collision_time = 0
    player.life = 6
    player.x = 350
    player.y = 380
    player.rect = player.imgs[0].get_rect(topleft=(player.x, player.y))
    playerframe = 0
    player.rect.left = player.x
    player.rect.top = player.y

### Gegner ###
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imgs_single_enemy = [pygame.image.load("graphics/enemies/single/enemy1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/enemy2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/enemy3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/enemy4.png").convert_alpha()]
        self.img_single_enemy_20p = [pygame.image.load("graphics/enemies/single/20p/enemy1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/20p/enemy2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/20p/enemy3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/20p/enemy4.png").convert_alpha()]
        self.img_single_enemy_40p = [pygame.image.load("graphics/enemies/single/40p/enemy1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/40p/enemy2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/40p/enemy3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/40p/enemy4.png").convert_alpha()]
        self.img_single_enemy_60p = [pygame.image.load("graphics/enemies/single/60p/enemy1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/60p/enemy2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/60p/enemy3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/60p/enemy4.png").convert_alpha()]
        self.img_single_enemy_80p = [pygame.image.load("graphics/enemies/single/80p/enemy1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/80p/enemy2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/80p/enemy3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/single/80p/enemy4.png").convert_alpha()]
        self.imgs_long_row_enemy = [pygame.image.load("graphics/enemies/long_row/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/enemies4.png").convert_alpha()]
        self.imgs_long_row_enemy_20p = [pygame.image.load("graphics/enemies/long_row/20p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/20p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/20p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/20p/enemies4.png").convert_alpha()]
        self.imgs_long_row_enemy_40p = [pygame.image.load("graphics/enemies/long_row/40p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/40p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/40p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/40p/enemies4.png").convert_alpha()]
        self.imgs_long_row_enemy_60p = [pygame.image.load("graphics/enemies/long_row/60p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/60p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/60p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/60p/enemies4.png").convert_alpha()]
        self.imgs_long_row_enemy_80p = [pygame.image.load("graphics/enemies/long_row/80p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/80p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/80p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/long_row/80p/enemies4.png").convert_alpha()]
        self.imgs_short_row_enemy = [pygame.image.load("graphics/enemies/short_row/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/enemies4.png").convert_alpha()]
        self.imgs_short_row_enemy_20p = [pygame.image.load("graphics/enemies/short_row/20p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/20p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/20p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/20p/enemies4.png").convert_alpha()]
        self.imgs_short_row_enemy_40p = [pygame.image.load("graphics/enemies/short_row/40p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/40p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/40p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/40p/enemies4.png").convert_alpha()]
        self.imgs_short_row_enemy_60p = [pygame.image.load("graphics/enemies/short_row/60p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/60p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/60p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/60p/enemies4.png").convert_alpha()]
        self.imgs_short_row_enemy_80p = [pygame.image.load("graphics/enemies/short_row/80p/enemies1.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/80p/enemies2.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/80p/enemies3.png").convert_alpha(),
                                  pygame.image.load("graphics/enemies/short_row/80p/enemies4.png").convert_alpha()]
        self.rect_6uhr = pygame.Rect(300, 500, 200, 50)
        self.rect_7uhr = pygame.Rect(180, 440, 50, 50)
        self.rect_9uhr = pygame.Rect(140, 210, 50, 180)
        self.rect_11uhr = pygame.Rect(180, 100, 50, 50)
        self.rect_12uhr = pygame.Rect(300, 35, 200, 50)
        self.rect_1uhr = pygame.Rect(600, 100, 50, 50)
        self.rect_3uhr = pygame.Rect(660, 210, 50, 180)
        self.rect_5uhr = pygame.Rect(600, 440, 50, 50)
        self.enemies = [self.rect_6uhr, self.rect_7uhr, self.rect_9uhr, self.rect_11uhr, self.rect_12uhr, self.rect_1uhr, self.rect_3uhr, self.rect_5uhr]
        self.enemy_no = 0
        self.enemy_spawned = False
        self.spawn_timer = 0
        self.enemy_frame_counter = 0
        self.which_enemy = 0
        self.x = 0
        self.y = 0

    def enemy_spawning(self):  # Zufallsgenerator, WELCHER Gegner spawnen soll
        self.which_enemy = random.uniform(1, 100)
        if self.which_enemy <= 12.5:
            self.enemy_no = 0
        elif self.which_enemy > 12.5 and self.which_enemy <= 25:
            self.enemy_no = 1
        elif self.which_enemy > 25 and self.which_enemy <= 37.5:
            self.enemy_no = 2
        elif self.which_enemy > 37.5 and self.which_enemy <= 50:
            self.enemy_no = 3
        elif self.which_enemy > 50 and self.which_enemy <= 62.5:
            self.enemy_no = 4
        elif self.which_enemy > 62.5 and self.which_enemy <= 75:
            self.enemy_no = 5
        elif self.which_enemy > 75 and self.which_enemy <= 87.5:
            self.enemy_no = 6
        elif self.which_enemy > 87.5 and self.which_enemy <= 100:
            self.enemy_no = 7
        self.spawn_timer = pygame.time.get_ticks()
        self.enemy_spawned = True

    def enemy_framing(self):
        if self.enemy_no == 1:  # single enemy 7 uhr
            if self.x == 0 and self.y == 0:
                self.x = 372
                self.y = 315
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.img_single_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.img_single_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.img_single_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.img_single_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x -= 6
            self.y += 4
        elif self.enemy_no == 3:  # single enemy 11 uhr
            if self.x == 0 and self.y == 0:
                self.x = 372
                self.y = 271
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.img_single_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.img_single_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.img_single_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.img_single_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x -= 6
            self.y -= 5
        elif self.enemy_no == 5:  # single enemy 1 uhr
            if self.x == 0 and self.y == 0:
                self.x = 420
                self.y = 271
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.img_single_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.img_single_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.img_single_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.img_single_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x += 6
            self.y -= 5
        elif self.enemy_no == 7:  # single enemy 5 uhr
            if self.x == 0 and self.y == 0:
                self.x = 420
                self.y = 315
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.img_single_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.img_single_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.img_single_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.img_single_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x += 6
            self.y += 4
        elif self.enemy_no == 2:  # short row enemies 9 uhr
            if self.x == 0 and self.y == 0:
                self.x = 370
                self.y = 290
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.imgs_short_row_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.imgs_short_row_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.imgs_short_row_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.imgs_short_row_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x -= 6
            self.y -= 2
        elif self.enemy_no == 6:  # short row enemies 3 uhr
            if self.x == 0 and self.y == 0:
                self.x = 425
                self.y = 290
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.imgs_short_row_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.imgs_short_row_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.imgs_short_row_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.imgs_short_row_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x += 6
            self.y -= 2
        elif self.enemy_no == 0:  # long row enemies 6 uhr
            if self.x == 0 and self.y == 0:
                self.x = 382
                self.y = 310
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.imgs_long_row_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.imgs_long_row_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.imgs_long_row_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.imgs_long_row_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x -= 1.5
            self.y += 5
        elif self.enemy_no == 4:  # long row enemies 12 uhr
            if self.x == 0 and self.y == 0:
                self.x = 384
                self.y = 281
            if pygame.time.get_ticks() - self.spawn_timer <= 375:
                screen.blit(self.imgs_long_row_enemy_20p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 375 and pygame.time.get_ticks() - self.spawn_timer <= 750:
                screen.blit(self.imgs_long_row_enemy_40p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 750 and pygame.time.get_ticks() - self.spawn_timer <= 1000:
                screen.blit(self.imgs_long_row_enemy_60p[round(self.enemy_frame_counter)], (self.x, self.y))
            elif pygame.time.get_ticks() - self.spawn_timer > 1000 and pygame.time.get_ticks() - self.spawn_timer <= 1200:
                screen.blit(self.imgs_long_row_enemy_80p[round(self.enemy_frame_counter)], (self.x, self.y))
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
            self.x -= 1.6
            self.y -= 6.1

    def enemy_drawing(self):
        if self.enemy_no == 1 or self.enemy_no == 3 or self.enemy_no == 5 or self.enemy_no == 7:  # single enemy
            screen.blit(self.imgs_single_enemy[round(self.enemy_frame_counter)], self.enemies[self.enemy_no])
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
        elif self.enemy_no == 0 or self.enemy_no == 4:  # enemy long row
            screen.blit(self.imgs_long_row_enemy[round(self.enemy_frame_counter)], self.enemies[self.enemy_no])
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1
        elif self.enemy_no == 2 or self.enemy_no == 6:  # enemy long row
            screen.blit(self.imgs_short_row_enemy[round(self.enemy_frame_counter)], self.enemies[self.enemy_no])
            if self.enemy_frame_counter > 3.3:
                self.enemy_frame_counter = 0
            self.enemy_frame_counter += 0.1

    def destroy(self):
        if self.enemy_spawned and pygame.time.get_ticks() - self.spawn_timer >= 2500:
            self.kill()
enemy1 = Enemy()
enemy2 = Enemy()
enemy3 = Enemy()
enemy4 = Enemy()
enemy5 = Enemy()
enemy6 = Enemy()
enemy7 = Enemy()
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7]
enemy = Enemy()

def enemy_reset():
    enemies[0].enemy_spawned = False
    enemies[1].enemy_spawned = False
    enemies[2].enemy_spawned = False
    enemies[3].enemy_spawned = False
    enemies[4].enemy_spawned = False
    enemies[5].enemy_spawned = False
    enemies[6].enemy_spawned = False
    enemies[0].spawn_timer = 0
    enemies[1].spawn_timer = 0
    enemies[2].spawn_timer = 0
    enemies[3].spawn_timer = 0
    enemies[4].spawn_timer = 0
    enemies[5].spawn_timer = 0
    enemies[6].spawn_timer = 0
    enemies[0].x = 0
    enemies[0].y = 0
    enemies[1].x = 0
    enemies[1].y = 0
    enemies[2].x = 0
    enemies[2].y = 0
    enemies[3].x = 0
    enemies[3].y = 0
    enemies[4].x = 0
    enemies[4].y = 0
    enemies[5].x = 0
    enemies[5].y = 0
    enemies[6].x = 0
    enemies[6].y = 0
    enemies[0].destroy()
    enemies[1].destroy()
    enemies[2].destroy()
    enemies[3].destroy()
    enemies[4].destroy()
    enemies[5].destroy()
    enemies[6].destroy()

### BG ###
class Tunnelframes:
    def __init__(self):
        self.bg_frame1 = pygame.image.load("graphics/tunnel/bg1.png").convert()
        self.bg_frame2 = pygame.image.load("graphics/tunnel/bg2.png").convert()
        self.bg_frame3 = pygame.image.load("graphics/tunnel/bg3.png").convert()
        self.bg_frame4 = pygame.image.load("graphics/tunnel/bg4.png").convert()
        self.bg_frame5 = pygame.image.load("graphics/tunnel/bg5.png").convert()
        self.bg_frame6 = pygame.image.load("graphics/tunnel/bg6.png").convert()
        self.bg_frame7 = pygame.image.load("graphics/tunnel/bg7.png").convert()
        self.bg_frame8 = pygame.image.load("graphics/tunnel/bg8.png").convert()
        self.bg_frame9 = pygame.image.load("graphics/tunnel/bg9.png").convert()
        self.bg_frame10 = pygame.image.load("graphics/tunnel/bg10.png").convert()
        self.bg_frame11 = pygame.image.load("graphics/tunnel/bg11.png").convert()
        self.bg_frame12 = pygame.image.load("graphics/tunnel/bg12.png").convert()
        self.bg_frame13 = pygame.image.load("graphics/tunnel/bg13.png").convert()
        self.bg_frame14 = pygame.image.load("graphics/tunnel/bg14.png").convert()
        self.bg_frame15 = pygame.image.load("graphics/tunnel/bg15.png").convert()
        self.bg_frame16 = pygame.image.load("graphics/tunnel/bg16.png").convert()
        self.bg_frame17 = pygame.image.load("graphics/tunnel/bg17.png").convert()
        self.bg_frame18 = pygame.image.load("graphics/tunnel/bg18.png").convert()
        self.bg_frame19 = pygame.image.load("graphics/tunnel/bg19.png").convert()
        self.bg_frame20 = pygame.image.load("graphics/tunnel/bg20.png").convert()
        self.bg_frame21 = pygame.image.load("graphics/tunnel/bg21.png").convert()
        self.bg_frame22 = pygame.image.load("graphics/tunnel/bg22.png").convert()
        self.bg_frame23 = pygame.image.load("graphics/tunnel/bg23.png").convert()
        self.bg_frame24 = pygame.image.load("graphics/tunnel/bg24.png").convert()
        self.bg_frame25 = pygame.image.load("graphics/tunnel/bg25.png").convert()
        self.bg_frame26 = pygame.image.load("graphics/tunnel/bg26.png").convert()
        self.bg_frame27 = pygame.image.load("graphics/tunnel/bg27.png").convert()
        self.bg_frame28 = pygame.image.load("graphics/tunnel/bg28.png").convert()
        self.bg_frame29 = pygame.image.load("graphics/tunnel/bg29.png").convert()
        self.frames = [self.bg_frame1, self.bg_frame2, self.bg_frame3, self.bg_frame4, self.bg_frame5, self.bg_frame6,
                       self.bg_frame7, self.bg_frame8, self.bg_frame9, self.bg_frame10, self.bg_frame11,
                       self.bg_frame12, self.bg_frame13, self.bg_frame14, self.bg_frame15, self.bg_frame16,
                       self.bg_frame17, self.bg_frame18, self.bg_frame19, self.bg_frame20, self.bg_frame21,
                       self.bg_frame22, self.bg_frame23, self.bg_frame24, self.bg_frame25, self.bg_frame26,
                       self.bg_frame27, self.bg_frame28, self.bg_frame29]

bg = Tunnelframes()
# BG-Farbe (die Transparent ueber die farblosen BG-Frames in der Gameloop gestuelpt wird)
bg_rect = pygame.Surface((800, 600))    # erstmal ein neues Surface erstellt (in Spielfenstergroesse)
bg_rect.set_alpha(128)                  # das Surface transparent setzen
red = 32
green = 158
blue = 12

def trans_bg():
    global red, green, blue
    bg_color = (red,green,blue)                    # BG Color (Standard gruen), soll bei versch. Events veraendert werden
    bg_rect.fill(bg_color)                  # das Surface mit einer RGB Farbe fuellen

framecounter = 0
framecounter_addition = 0.8
def bg_framing():
    global framecounter
    screen.blit(bg.frames[round(framecounter)], (0, 0))
    if round(framecounter + framecounter_addition) >= 29:
        framecounter = 0
    else:
        framecounter += framecounter_addition

def display_score():
    playtime = int((pygame.time.get_ticks() / 1000) - start_time)
    score_surf = mario64_font.render("Score: " + str(playtime), False, (0, 0, 0))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return playtime

## Info Screen ##
title_surf = marioKart_font.render("Motor Rooter 16 bit", False, (255, 255, 255))
title_rect = title_surf.get_rect(center = (400, 50))
inst_surf = pixel_font.render("Press Space to jump into the tube!", False, (255, 255, 255))
inst_rect = inst_surf.get_rect(center=(400,500))
controls_img = pygame.image.load("graphics/controls.png").convert_alpha()
controls_rect = controls_img.get_rect(center=(400,300))


### Gameloop ###
score = 0
start_time = 0
playtime = 0
playerframe = 0
game_active = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if game_active != True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    enemy_reset()
                    player_reset()
                    hard_diff = False
                    super_hard_diff = False
                    extreme_hard_diff = False
                    red = 32
                    green = 158
                    blue = 12
                    game_active = True
                    start_time = (pygame.time.get_ticks() / 1000)
                    framecounter = 0
                    framecounter_addition = 0.8
                    title_music_played = False
                    title_music.stop()
                    game_music.play(loops=-1)
                    car_sfx.play(loops=-1)

    if game_active:
        player.player_input()

        if pygame.time.get_ticks() - player.collision_time > 3000:     # falls zuvor mit Gegner kollidiert, fuer 3 Sek immun
            player.collision_immune = False

        bg_framing()    # der animierte BG

        if hard_diff and super_hard_diff != True:
            if red + 11 >= 193:
                red = 193
            else: red += 11
            if blue + 2 >= 25:
                blue = 25
            else: blue += 2
            if green + 7 >= 205:
                green = 205
            else: green += 7
        if super_hard_diff and extreme_hard_diff != True:
            if red + 11 >= 193:
                red = 193
            else: red += 11
            if blue + 7 >= 205:
                blue = 205
            else: blue += 7
            if green + 2 >= 25:
                green = 25
            else: green += 2
        if extreme_hard_diff:
            if red + 3 >= 226:
                red = 226
            else: red += 3
            if blue - 15 <= 25:
                blue = 25
            else: blue -= 15

        trans_bg()
        screen.blit(bg_rect, (0,0))     # den transparenten BG-Farbwert blitten

        # ob die Gegner im Hintergrund erscheinen koennen
        if enemies[0].enemy_spawned and pygame.time.get_ticks() - enemies[0].spawn_timer < 1200:
            enemies[0].enemy_framing()
        if enemies[1].enemy_spawned and pygame.time.get_ticks() - enemies[1].spawn_timer < 1200:
            enemies[1].enemy_framing()
        if enemies[2].enemy_spawned and pygame.time.get_ticks() - enemies[2].spawn_timer < 1200:
            enemies[2].enemy_framing()
        if enemies[3].enemy_spawned and pygame.time.get_ticks() - enemies[3].spawn_timer < 1200:
            enemies[3].enemy_framing()
        if hard_diff == True:
            if enemies[4].enemy_spawned and pygame.time.get_ticks() - enemies[4].spawn_timer < 1200:
                enemies[4].enemy_framing()
        if super_hard_diff == True:
            if enemies[5].enemy_spawned and pygame.time.get_ticks() - enemies[5].spawn_timer < 1200:
                enemies[5].enemy_framing()
        if extreme_hard_diff == True:
            if enemies[6].enemy_spawned and pygame.time.get_ticks() - enemies[6].spawn_timer < 1200:
                enemies[6].enemy_framing()

        # Gegner blitten (falls gespawned)
        if enemies[0].enemy_spawned and pygame.time.get_ticks() - enemies[0].spawn_timer >= 1200:
            enemies[0].x = 0
            enemies[0].y = 0
            enemies[0].enemy_drawing()
        if enemies[1].enemy_spawned and pygame.time.get_ticks() - enemies[1].spawn_timer >= 1200:
            enemies[1].x = 0
            enemies[1].y = 0
            enemies[1].enemy_drawing()
        if enemies[2].enemy_spawned and pygame.time.get_ticks() - enemies[2].spawn_timer >= 1200:
            enemies[2].x = 0
            enemies[2].y = 0
            enemies[2].enemy_drawing()
        if enemies[3].enemy_spawned and pygame.time.get_ticks() - enemies[3].spawn_timer >= 1200:
            enemies[3].x = 0
            enemies[3].y = 0
            enemies[3].enemy_drawing()
        if hard_diff == True:
            if enemies[4].enemy_spawned and pygame.time.get_ticks() - enemies[4].spawn_timer >= 1200:
                enemies[4].x = 0
                enemies[4].y = 0
                enemies[4].enemy_drawing()
        if super_hard_diff == True:
            if enemies[5].enemy_spawned and pygame.time.get_ticks() - enemies[5].spawn_timer >= 1200:
                enemies[5].x = 0
                enemies[5].y = 0
                enemies[5].enemy_drawing()
        if extreme_hard_diff == True:
            if enemies[6].enemy_spawned and pygame.time.get_ticks() - enemies[6].spawn_timer >= 1200:
                enemies[6].x = 0
                enemies[6].y = 0
                enemies[6].enemy_drawing()

        # nach 0,5 Sekunden despawned der Gegner wieder
        if enemies[0].enemy_spawned and pygame.time.get_ticks() - enemies[0].spawn_timer >= 1700:
            enemies[0].enemy_spawned = False
            enemies[0].destroy()
        if enemies[1].enemy_spawned and pygame.time.get_ticks() - enemies[1].spawn_timer >= 1700:
            enemies[1].enemy_spawned = False
            enemies[1].destroy()
        if enemies[2].enemy_spawned and pygame.time.get_ticks() - enemies[2].spawn_timer >= 1700:
            enemies[2].enemy_spawned = False
            enemies[2].destroy()
        if enemies[3].enemy_spawned and pygame.time.get_ticks() - enemies[3].spawn_timer >= 1700:
            enemies[3].enemy_spawned = False
            enemies[3].destroy()
        if hard_diff == True:
            if enemies[4].enemy_spawned and pygame.time.get_ticks() - enemies[4].spawn_timer >= 1700:
                enemies[4].enemy_spawned = False
                enemies[4].destroy()
        if super_hard_diff == True:
            if enemies[5].enemy_spawned and pygame.time.get_ticks() - enemies[5].spawn_timer >= 1700:
                enemies[5].enemy_spawned = False
                enemies[5].destroy()
        if extreme_hard_diff == True:
            if enemies[6].enemy_spawned and pygame.time.get_ticks() - enemies[6].spawn_timer >= 1700:
                enemies[6].enemy_spawned = False
                enemies[6].destroy()

        if player.collision_immune:     # Spieler blitten
            player.inv_frames()
        else:
            screen.blit(player.imgs[playerframe], player.rect)

        score = display_score()  # score blitten

        player.draw_life()  # den Spielerlebenstand blitten

        if (pygame.time.get_ticks() / 1000) - start_time > 10:      # nach 10 Sek wirds schneller
            framecounter_addition = 1.4
            player.speed = 16
            hard_diff = True
            if (pygame.time.get_ticks() / 1000) - start_time <= 13:
                message_hard_surf_l1 = pixel_font.render("Not bad...", False, (186, 8, 8))
                message_gard_rect_l1 = message_hard_surf_l1.get_rect(center = (400, 280))
                screen.blit(message_hard_surf_l1, message_gard_rect_l1)
                message_hard_surf_l2 = pixel_font.render("How's about increasing the speed?", False, (186, 8, 8))
                message_gard_rect_l2 = message_hard_surf_l2.get_rect(center = (400, 300))
                screen.blit(message_hard_surf_l2, message_gard_rect_l2)
        if (pygame.time.get_ticks() / 1000) - start_time > 20:      # nach 20 Sek schneller
            framecounter_addition = 1.8
            player.speed = 20
            super_hard_diff = True
            if (pygame.time.get_ticks() / 1000) - start_time <= 23:
                message_hard_surf_l1 = pixel_font.render("Now you're making me angry...", False, (186, 8, 8))
                message_gard_rect_l1 = message_hard_surf_l1.get_rect(center = (400, 280))
                screen.blit(message_hard_surf_l1, message_gard_rect_l1)
                message_hard_surf_l2 = pixel_font.render("Speed up!", False, (186, 8, 8))
                message_gard_rect_l2 = message_hard_surf_l2.get_rect(center = (400, 300))
                screen.blit(message_hard_surf_l2, message_gard_rect_l2)
        if (pygame.time.get_ticks() / 1000) - start_time > 30:      # nach 30 Sek Endspeed und alle Gegner
            framecounter_addition = 2.5
            player.speed = 25
            extreme_hard_diff = True
            if (pygame.time.get_ticks() / 1000) - start_time <= 33:
                message_hard_surf_l1 = pixel_font.render("Hmpf...", False, (186, 8, 8))
                message_gard_rect_l1 = message_hard_surf_l1.get_rect(center = (400, 280))
                screen.blit(message_hard_surf_l1, message_gard_rect_l1)
                message_hard_surf_l2 = pixel_font.render("This game should end soon!", False, (186, 8, 8))
                message_gard_rect_l2 = message_hard_surf_l2.get_rect(center = (400, 300))
                screen.blit(message_hard_surf_l2, message_gard_rect_l2)
        if ((pygame.time.get_ticks() / 1000) - start_time) > 60 and ((pygame.time.get_ticks() / 1000) - start_time) <= 63:
            message_hard_surf_l1 = pixel_font.render("Still alive?", False, (186, 8, 8))
            message_gard_rect_l1 = message_hard_surf_l1.get_rect(center=(400, 280))
            screen.blit(message_hard_surf_l1, message_gard_rect_l1)
            message_hard_surf_l2 = pixel_font.render("You will never reach the end!", False, (186, 8, 8))
            message_gard_rect_l2 = message_hard_surf_l2.get_rect(center=(400, 300))
            screen.blit(message_hard_surf_l2, message_gard_rect_l2)
        if ((pygame.time.get_ticks() / 1000) - start_time) > 280 and ((pygame.time.get_ticks() / 1000) - start_time) <= 285:
            message_hard_surf_l1 = pixel_font.render("Actually...", False, (186, 8, 8))
            message_gard_rect_l1 = message_hard_surf_l1.get_rect(center=(400, 280))
            screen.blit(message_hard_surf_l1, message_gard_rect_l1)
            message_hard_surf_l2 = pixel_font.render("This is an endless runner.", False, (186, 8, 8))
            message_gard_rect_l2 = message_hard_surf_l2.get_rect(center=(400, 300))
            screen.blit(message_hard_surf_l2, message_gard_rect_l2)
            message_hard_surf_l3 = pixel_font.render("You'll never be able to reach an 'end'. ;)", False, (186, 8, 8))
            message_gard_rect_l3 = message_hard_surf_l3.get_rect(center=(400, 320))
            screen.blit(message_hard_surf_l3, message_gard_rect_l3)

        # Zufall, ob Gegner spawnen sollen (nur falls zZt kein aktiver Spawn vorhanden ist)
        if random.randrange(0, 100) < 5 and enemies[0].enemy_spawned != True:
            enemies[0].enemy_spawning()
        if random.randrange(0, 100) < 5 and enemies[1].enemy_spawned != True:
            enemies[1].enemy_spawning()
        if random.randrange(0, 100) < 5 and enemies[2].enemy_spawned != True:
            enemies[2].enemy_spawning()
        if random.randrange(0, 100) < 5 and enemies[3].enemy_spawned != True:
            enemies[3].enemy_spawning()
        if hard_diff == True:
            if random.randrange(0, 100) < 10 and enemies[4].enemy_spawned != True:
                enemies[4].enemy_spawning()
        if super_hard_diff == True:
            if random.randrange(0, 100) < 10 and enemies[5].enemy_spawned != True:
                enemies[5].enemy_spawning()
        if extreme_hard_diff == True:
            if random.randrange(0, 100) < 20 and enemies[6].enemy_spawned != True:
                enemies[6].enemy_spawning()

        # Kollision mit pygame rechnen lassen, seit wie vielen ms die Kollision stattfand
        if player.rect.colliderect(enemies[0].enemies[enemies[0].enemy_no]) and enemies[0].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[0].spawn_timer >= 1400:
            hit_sfx.play()
            if player.life == 1:
                game_active = False
            else:
                player.life -= 1
            player.collision_immune = True
            player.collision_time = pygame.time.get_ticks()
            enemies[0].enemy_spawned = False
        if player.rect.colliderect(enemies[1].enemies[enemies[1].enemy_no]) and enemies[1].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[1].spawn_timer >= 1400:
            hit_sfx.play()
            if player.life == 1:
                game_active = False
            else:
                player.life -= 1
            player.collision_immune = True
            player.collision_time = pygame.time.get_ticks()
            enemies[1].enemy_spawned = False
        if player.rect.colliderect(enemies[2].enemies[enemies[2].enemy_no]) and enemies[2].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[2].spawn_timer >= 1400:
            hit_sfx.play()
            if player.life == 1:
                game_active = False
            else:
                player.life -= 1
            player.collision_immune = True
            player.collision_time = pygame.time.get_ticks()
            enemies[2].enemy_spawned = False
        if player.rect.colliderect(enemies[3].enemies[enemies[3].enemy_no]) and enemies[3].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[3].spawn_timer >= 1400:
            hit_sfx.play()
            if player.life == 1:
                game_active = False
            else:
                player.life -= 1
            player.collision_immune = True
            player.collision_time = pygame.time.get_ticks()
            enemies[3].enemy_spawned = False
        if hard_diff == True:
            if player.rect.colliderect(enemies[4].enemies[enemies[4].enemy_no]) and enemies[
                4].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[
                4].spawn_timer >= 1400:
                hit_sfx.play()
                if player.life == 1:
                    game_active = False
                else:
                    player.life -= 1
                player.collision_immune = True
                player.collision_time = pygame.time.get_ticks()
                enemies[4].enemy_spawned = False
        if super_hard_diff == True:
            if player.rect.colliderect(enemies[5].enemies[enemies[5].enemy_no]) and enemies[
                5].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[
                5].spawn_timer >= 1400:
                hit_sfx.play()
                if player.life == 1:
                    game_active = False
                else:
                    player.life -= 1
                player.collision_immune = True
                player.collision_time = pygame.time.get_ticks()
                enemies[5].enemy_spawned = False
        if extreme_hard_diff == True:
            if player.rect.colliderect(enemies[6].enemies[enemies[6].enemy_no]) and enemies[
                6].enemy_spawned and player.collision_immune != True and pygame.time.get_ticks() - enemies[
                6].spawn_timer >= 1400:
                hit_sfx.play()
                if player.life == 1:
                    game_active = False
                else:
                    player.life -= 1
                player.collision_immune = True
                player.collision_time = pygame.time.get_ticks()
                enemies[6].enemy_spawned = False
    else:   ## infoscreen
        screen.fill((147, 28, 171))
        screen.blit(title_surf, title_rect)

        if title_music_played != True:      # damit die Titelmusik nicht bei jedem Durchlauf neu gestartet wird
            game_music.stop()
            car_sfx.stop()
            title_music.play(loops=-1)
            title_music_played = True

        score_message_surf = pixel_font.render("Your Score: " + str(score), False, (255, 255, 255))
        score_message_rect = score_message_surf.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(inst_surf, inst_rect)
            screen.blit(controls_img, controls_rect)
        else:
            screen.blit(score_message_surf, score_message_rect)

    pygame.display.update()
    clock.tick(30)
