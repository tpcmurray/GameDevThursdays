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

# Load beam
beam_img = pygame.image.load(os.path.join("assets", "beam.png")).convert_alpha()

# Load laser sounds
laser_sounds = [
    pygame.mixer.Sound(os.path.join("assets", "laser1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "laser2.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "laser3.mp3"))
]

# Load explosion image and sound
# TODO 1: Load explosion image, same as line 35, but for explosion.png
# TODO 2: Load explosion sound, similar to how laser sounds are loaded. explosion.wav is the sound file

# Function to create explosion frames
# TODO 3: Create a list of explosion frames by splitting the explosion image into 5 frames of 128x128 pixels each
#       and storing them in a list. You'll need the subsurface method, like lines 24-26.

# Load background
background = pygame.image.load('assets/background.png')
background1_y = 0
background2_y = -background.get_height()
background_speed = 2

# variables
speed = 2
enemies = []  # List to store enemies - each enemy will be [rect, x_speed]
beams = []    # List to store active beams
# TODO 4: Add another list variable to keep track of the explosions. 
count_frames = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new beam
                beam_rect = beam_img.get_rect()
                beam_rect.centerx = ship_rect.centerx
                beam_rect.bottom = ship_rect.top
                beams.append(beam_rect)
                
                # Play random laser sound
                random.choice(laser_sounds).play()

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
    
    # Move beams up
    for beam in beams[:]:
        beam.y -= 5  # Move beam up the screen
        if beam.bottom < 0:  # Remove if off screen (top)
            beams.remove(beam)

    # Check for collisions between beams and enemies
    # TODO 5: Start with a for loop, looping through the beams, same as line 129
    # TODO 6: Inside the loop, add another for loop to loop through the enemies
    # TODO 7: Inside the enemy loop, check IF the beam collides with the enemy, using the colliderect method: beam.colliderect(enemy[0]):
    # TODO 8: If there is a collision:
    #   remove the beam its list
    #   remove the enemy from its list
    #   add an explosion at the enemy's position
    #       the explosion array should be a list with the enemy's top left position, the current frame of the explosion, which is 0, and the current time
    #   play the explosion sound

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
        
    # Draw all beams
    for beam in beams:
        screen.blit(beam_img, beam)

    # Draw all explosions
    # TODO 9: record the current time
    # TODO 10: loop through the explosions list
    # TODO 11: if the current time - the explosion's start time is greater than 20 (milliseconds), move to the next frame
    # TODO 12: if the frame is greater than the length of the explosion frames (we are past the last frame), remove the explosion
    # TODO 13: otherwise, draw the explosion frame as is

    # Update the display
    pygame.display.flip()

pygame.quit()