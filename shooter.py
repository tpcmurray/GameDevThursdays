import pygame
import os
import random

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

# Load enemy
enemy_img = pygame.image.load(os.path.join("assets", "enemy1.png")).convert_alpha()

# TODO 1: Load beam (like line 32)

# TODO 2: Load 2 laser sounds into a list (see: pygame.mixer.Sound)

# Load background
background = pygame.image.load('assets/background.png')
background1_y = 0
background2_y = -background.get_height()
background_speed = 2

# variables
speed = 2
enemies = []  # List to store enemies - each enemy will be [rect, x_speed]
# TODO 3: a List to store beams, same as enemies above
count_frames = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO 4: Check for space key press to create a new beam
        #   1. Create a new beam
        #   2. set the beams x and y to the ship's nose x and y
        #   3. Add the beam to the list of beams
        # TODO 5: Play a random laser sound when a beam is created

    # Update the frame counter
    count_frames += 1
    if count_frames > 60:  # Reset frame counter every 60 frames
        count_frames = 0    

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

    # Spawn a new enemy
    if count_frames >= 60:                     # Spawn enemy every 60 frames
        enemy_rect = enemy_img.get_rect()      # the sprite

        # Randomize the enemy's position and speed
        enemy_rect.x = random.randint(0, screen_width - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height
        x_speed = random.uniform(-1, 1)
        if x_speed < .5 and x_speed > -.5:
            x_speed = 1

        # Add the enemy to the list
        enemies.append([enemy_rect, x_speed])

    # Move enemies down
    for enemy in enemies[:]:
        enemy_rect = enemy[0]
        x_speed = enemy[1]
        enemy_rect.x += x_speed  # Move horizontally based on x_speed
        enemy_rect.y += 2        # Move down the screen 2 pixels
        
        # Remove if off screen (bottom or sides)
        if enemy_rect.top > screen_height or enemy_rect.left < -50 or enemy_rect.right > screen_width + 50:
            enemies.remove(enemy)
    
    # TODO 6: Move beams up the screen and remove if off screen (top)
    #    This is very similar to the code above for moving enemies

    # scroll the background before drawing it, along the y axis
    background1_y += background_speed
    background2_y += background_speed
    if background1_y > screen_height: # if the background is off the screen, reset it
        background1_y = -background.get_height()
    if background2_y > screen_height: # if the background is off the screen, reset it
        background2_y = -background.get_height()

    # Draw everything
    screen.blit(background, (0, background1_y))
    screen.blit(background, (0, background2_y))
    screen.blit(ship, ship_rect)
    
    # Draw all enemies
    for enemy in enemies:
        screen.blit(enemy_img, enemy[0])
        
    # TODO 7: Draw all beams
    #    This is very similar to the code above for drawing enemies

    # Update the display
    pygame.display.flip()

pygame.quit()