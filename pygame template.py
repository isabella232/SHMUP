import pygame as pg
import random

# Constants
RES = [600, 800]
FPS = 30

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pg.init()
pg.mixer.init()
SCREEN = pg.display.set_mode(RES)
pg.display.set_caption("AstroidShooter")
clock = pg.time.Clock()

# Create the sprite groups
allSprites = pg.sprite.Group()

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
    screen.fill(BLACK)
    allSprites.draw(SCREEN)

    # AFTER drawining everything, flip the display.
    pg.display.flip()
