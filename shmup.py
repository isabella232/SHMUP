# ################################################# #
# Author: Paul Duncan 2019 July 10
# Tutorial used: https://www.youtube.com/playlist?list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw
# Sprites used: https://opengameart.org/content/space-shooter-redux
# ################################################# #
# Import needed libraries.
# ################################################# #
import pygame as pg
import random
from os import path

# ################################################# #
# Constants
# ################################################# #
WIDTH = 600
HEIGHT = 800
FPS = 60
volume = .5
speed = 12
score = 0
# ################################################# #
# Media Folders
# ################################################# #
img_folder = path.join(path.dirname(__file__), 'img')
snd_folder = path.join(path.dirname(__file__), 'snd')
# ################################################# #
# Define Colors
# ################################################# #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font_name = pg.font.match_font('arial')


def drawText(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def mediaLoad(media):
    m = pg.image.load(path.join(img_folder, media)).convert()
    return m


def spawnMobs():
    m = Mob()
    allSprites.add(m)
    mobs.add(m)


def drawShieldBar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct / 100 * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_bar = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_bar)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pg.sprite.Sprite):
    """Sprite class for the player"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(mediaLoad("playerShip1_blue.png"), (50, 38))
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()

    def update(self):
        self.speedx = 0
        k = pg.key.get_pressed()
        if k[pg.K_a]:
            self.speedx = -speed
        if k[pg.K_d]:
            self.speedx = speed
        if k[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            shoot_sound.play()
            self.laser = Lasers(self.rect.centerx, self.rect.top + 5)
            allSprites.add(self.laser)
            lasers.add(self.laser)


class Mob(pg.sprite.Sprite):
    """Sprite class for the player"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.image_orig.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image_orig)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-1250.0, -150.0)
        self.width = self.image.get_width()
        self.speedy = random.randrange(2, 15)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-6, 6)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 20:
            self.last_update = now
            self.rot = self.rot + self.rot_speed % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-1150.0, -100.0)
            self.speedy = random.randrange(4, 14)
            self.speedx = random.randrange(-3, 3)


class Lasers(pg.sprite.Sprite):
    """Sprite class for the player"""
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = mediaLoad("laserBlue01.png")
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    """Sprite class for the explosions"""
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explos_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explos_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explos_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# ################################################# #
# Initialize pygame & create window
#region ########################################### #
pg.mixer.pre_init(44100, -16, 2, 1024)
pg.mixer.init()
pg.init()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AstroidShooter")
clock = pg.time.Clock()

#endregion ######################################## #
# Load Media
#region ########################################### #
shoot_sound = pg.mixer.Sound(path.join(snd_folder, "Laser_Shoot27.wav"))
shoot_sound.set_volume(volume * .3)
bg = pg.transform.scale(mediaLoad("bg5.jpg"), (WIDTH, HEIGHT))
bg_rect = bg.get_rect()

explos_anim = {}
explos_anim['hu'] = []
explos_anim['lg'] = []
explos_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = mediaLoad(filename)
    img.set_colorkey(BLACK)
    img_hu = pg.transform.scale(img, (100, 100))
    explos_anim['hu'].append(img_hu)
    img_lg = pg.transform.scale(img, (75, 75))
    explos_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explos_anim['sm'].append(img_sm)
print(explos_anim)
# explos_anim = ['regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png',
#               'regularExplosion03.png', 'regularExplosion04.png', 'regularExplosion05.png',
 #              'regularExplosion06.png', 'regularExplosion07.png', 'regularExplosion08.png']


meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
               'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
               'meteorBrown_tiny2.png', 'meteorGrey_big1.png', 'meteorGrey_big2.png',
               'meteorGrey_big3.png', 'meteorGrey_big4.png', 'meteorGrey_med1.png',
               'meteorGrey_med2.png', 'meteorGrey_small1.png', 'meteorGrey_small2.png',
               'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png', ]
for img in meteor_list:
    meteor_images.append(mediaLoad(img))

num_images = []
num_list = ['numeral0.png', 'numeral1.png', 'numeral2.png', 'numeral3.png', 'numeral4.png',
            'numeral5.png', 'numeral6.png', 'numeral7.png', 'numeral8.png', 'numeral9.png', ]
for num in num_list:
    num_images.append(mediaLoad(num))

explo_snds = []
for explo in ['Explosion17.wav', 'Explosion28sm.wav', 'Explosion50sm.wav']:
    print(path.join(snd_folder, explo))
    explo_snds.append(pg.mixer.Sound(path.join(snd_folder, explo)))
    for s in explo_snds:
        s.set_volume(volume * .3)

pg.mixer.music.load(path.join(snd_folder, "through space.ogg"))
pg.mixer.music.set_volume(volume * .9)
pg.mixer.music.play(loops=-1)

#endregion ######################################## #
# Create sprite groups
#region ########################################### #
allSprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lasers = pg.sprite.Group()

#endregion ########################################### #
# Create sprite objects
#region ########################################### #
player = Player()
for x in range(20):
    spawnMobs()

#endregion ########################################### #
# Add sprite objects to sprite groups
#region ########################################### #

allSprites.add(player)

#endregion ########################################### #
# Game Loop
#region ########################################### #
gameRunning = True
while gameRunning:
    # Keep running at set framerate speed.
    clock.tick(FPS)
    # Process input (events)
    for e in pg.event.get():
        # Check to close window
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            gameRunning = False

    # ################################################# #
    # Update - Use update def from sprite group classes
    # ################################################# #
    allSprites.update()

    # ################################################# #
    # COLLISION - Code when collision happends
    # ################################################# #
    # BULLET COLLISION ON MOBS
    laserhits = pg.sprite.groupcollide(mobs, lasers, True, True, pg.sprite.collide_mask)
    for hit in laserhits:
        score += round(50 - hit.width / 3)
        random.choice(explo_snds).play()
        expl = Explosion(hit.rect.center, 'lg')
        allSprites.add(expl)
        spawnMobs()

    # MOB COLLISION ON PLAYER
    mobhits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_mask)
    for hit in mobhits:
        player.health -= hit.width / 50
        if hit.width < 30:
            expl = Explosion(hit.rect.center, 'sm')
            allSprites.add(expl)
            print("SM: " + str(hit.width))
        elif hit.width >= 30 and hit.width < 80:
            expl = Explosion(hit.rect.center, 'lg')
            allSprites.add(expl)
            print("BIG: " + str(hit.width))
        elif hit.width > 80:
            expl = Explosion(hit.rect.center, 'hu')
            allSprites.add(expl)
            print("HUGE: " + str(hit.width))
        spawnMobs()

    if player.health < 1:
        gameRunning = False

    # ################################################# #
    # Draw / Render. Fill the backgroun then draw the
    # sprites from the sprite group.
    # ################################################# #
    SCREEN.fill(BLACK)
    SCREEN.blit(bg, bg_rect)
    allSprites.draw(SCREEN)
    drawText(SCREEN, str(score), 20, WIDTH / 2, 10)
    SCREEN.blit(num_images[0], num_images[0].get_rect())
    drawShieldBar(SCREEN, 5, 5, player.health)

    # ################################################# #
    # AFTER drawining everything, flip the display.
    # ################################################# #
    pg.display.flip()
