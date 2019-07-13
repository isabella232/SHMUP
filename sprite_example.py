import pygame as pg
import random
import os

# Constants
RES = [600, 800]
FPS = 30
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pg.sprite.Sprite):
    # Sprite class for the player
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "playerShip1_blue.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (RES[0] / 2, RES[1] / 2)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > RES[1] - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > RES[0]:
            self.rect.right = 0

# Initialize pygame & create window
pg.init()
pg.mixer.init()
SCREEN = pg.display.set_mode(RES)
pg.display.set_caption("AstroidShooter")
clock = pg.time.Clock()

# Create the sprite groups
allSprites = pg.sprite.Group()
# Create sprite objects
for x in range(10):
    player = Player()
    # Add sprite objects to groups
    allSprites.add(player)

# Game Loop
gameRunning = True
while gameRunning:
    # Keep running at set framerate speed.
    clock.tick(FPS)
    # Process input (events)
    for e in pg.event.get():
        # Check to close window
        if e.type == pg.QUIT:
            gameRunning = False

    # Update
    allSprites.update()

    # Draw / Render
    SCREEN.fill(BLUE)
    allSprites.draw(SCREEN)

    # AFTER drawining everything, flip the display.
    pg.display.flip()
