import pygame
import os
# TODO 1: we need to import 'random' to generate random numbers

from pygame.mixer import music

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 700  # Set the width of the window
screen_height = 1000  # Set the height of the window
screen = pygame.display.set_mode((screen_width, screen_height))

# load, play, and loop music at 50% volume
music.load(os.path.join("assets", "backtrack.mp3"))
music.set_volume(0.5)  # Set volume to 50% (0 to 1)
music.play(-1)  # -1 means loop indefinitely

# load ship sprite sheet, load 3 ship images. the image is 192 x 64. all images are 64x64
sprite_sheet = pygame.image.load(os.path.join("assets", "ship.png")).convert_alpha()
sprite_width = sprite_sheet.get_width() // 3  # Divide by 3 since there are 3 frames
sprite_height = sprite_sheet.get_height()
ship_left = sprite_sheet.subsurface((0, 0, sprite_width, sprite_height))
ship_center = sprite_sheet.subsurface((sprite_width, 0, sprite_width, sprite_height))
ship_right = sprite_sheet.subsurface((sprite_width * 2, 0, sprite_width, sprite_height))
ship = ship_center

ship_rect = ship.get_rect(center=(screen_width // 2, screen_height  - 50))

# TODO 2: load the enemy sprite, same as line 21

# Load background
background = pygame.image.load('assets/background.png')
background1_y = 0
background2_y = -background.get_height()
background_speed = 2

# variables
speed = 2
# TODO 3: create an ARRAY to store all enemy sprite TUPLES [rect, x_speed (sideways movement)] 
# TODO 4: create a simple variable to store the frane count

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# TODO 5: keep track of the frame count. every 60 frames or greater, reset to zero

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ship_rect.y -= speed
    if keys[pygame.K_DOWN]:
        ship_rect.y += speed

    # this section is an if, elif, else block to determine which image to use
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
        ship = ship_left
    elif keys[pygame.K_RIGHT]:
        ship_rect.x += speed
        ship = ship_right
    else:
        ship = ship_center

# TODO 6: spawn a new enemy every 60 frames
    # randomize enemy position and speed
    # add the enemy to your array, so you can track it

# TODO 7: move enemies down the screen at y +2 
    # loop through all enemies, and move them down the screen
    # read out (from the tuple) the enemy rect and the x axis speed
    # remove enemies that are off the screen (check against screen width and height)


    # scroll the background before drawing it, along the y axis
    background1_y += background_speed
    background2_y += background_speed
    if background1_y > screen_height: # if the background is off the screen, reset it
        background1_y = -background.get_height()
    if background2_y > screen_height: # if the background is off the screen, reset it
        background2_y = -background.get_height()

    # Draw the two copies of the background
    screen.blit(background, (0, background1_y))
    screen.blit(background, (0, background2_y))

    # Draw the ship
    screen.blit(ship, ship_rect)

# TODO : draw all the enemies. same as drawing the ship, but in a loop

    # Update the display
    pygame.display.flip()

pygame.quit()
