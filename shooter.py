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
explosion_img = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
explosion_sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))

# Function to create explosion frames
explosion_frames = [explosion_img.subsurface((i * 128, 0, 128, 128)) for i in range(5)]

# Load background
background = pygame.image.load('assets/background.png')
background1_y = 0
background2_y = -background.get_height()
background_speed = 0.5

# TODO 1: Load projectile sprite (see same as line 35)

# TODO 2: Load FONT!
# use file font.tff in the assets folder. 
# To load it, see the pygame.font.Font() function at: https://www.pygame.org/docs/ref/font.html#pygame.font.Font
# you'll want to also specify the size of the font. try 36 to start, and make it as big or small as you like.

# variables
speed = 2
enemies = []  # List to store enemies - each enemy will be [rect, x_speed]
beams = []    # List to store active beams
explosions = []  # List to store active explosions
count_frames = 0
spawn_enemies_every = 200  # Spawn an enemy every so many frames

# TODO 3: create variables as follows:
# player_health, set to 100
# score, set to 0
# enemy_bullets, which is an empty list same as line 67

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
    if count_frames > spawn_enemies_every:  # Reset frame counter
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
    if count_frames >= spawn_enemies_every:                   # Spawn enemy every so many frames
        enemy_rect = enemy_img.get_rect()      # the sprite

        # Randomize the enemy's position and speed
        enemy_rect.x = random.randint(0, screen_width - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height
        x_speed = random.uniform(-2, 2)
        if x_speed < .1 and x_speed > -.1:
            x_speed = .3

        # Add the enemy to the list
        enemies.append([enemy_rect, x_speed, enemy_rect.x, enemy_rect.y])

        # TODO 4: sometimes enemies shoot.
        # loop through all enemies
        #   for each enemy, randomly decide if they shoot
        #       if they shoot, create a new bullet (see line 117)
        #       set the bullet's position to the enemy's position
        #       (optional bonus points, have the bullet move towards the player, instead of straight down!)
        #       add the bullet to the enemy_bullets list

    # Move enemies down
    for enemy in enemies[:]:
        enemy_rect = enemy[0]
        x_speed = enemy[1]

        enemy[2] += x_speed                      # Update the original x position
        enemy[3] += 1.0 * random.uniform(1, 2)  # Enemy speed, randomized
        
        enemy_rect.x = enemy[2]  # Move horizontally based on x_speed
        enemy_rect.y = enemy[3]  # Move vertically
        
        # reverse direction if enemy hits the edge of the screen
        if enemy_rect.x <= 0 or enemy_rect.x > screen_width - enemy_rect.width:
            enemy[1] = -enemy[1]
    
    # Move beams up
    for beam in beams[:]:
        beam.y -= 5  # Move beam up the screen
        if beam.bottom < 0:  # Remove if off screen (top)
            beams.remove(beam)

    # TODO 5: Move enemy bullets 
    # loop through all enemy bullets
    #   for each bullet, move it across the screen (change its X and or Y value)
    #   
    #   check if bullet collides with player (see line 170)
    #      if it does, remove the bullet and decrease player_health by 25
    #      if player_health is less than or equal to 0, end the game (set running = false)
    #   else, if bullet is off the screen remove it from the list

    # Check for collisions between beams and enemies
    for beam in beams[:]:
        for enemy in enemies[:]:
            if beam.colliderect(enemy[0]):
                beams.remove(beam)
                enemies.remove(enemy)
                explosions.append([enemy[0].topleft, 0, pygame.time.get_ticks()])  # Add explosion at enemy position
                explosion_sound.play()
                break

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
        
    # TODO 6: Draw all enemy bullets. (copy enemy drawing just above)
    
    # Draw all beams
    for beam in beams:
        screen.blit(beam_img, beam)

    # Draw all explosions
    current_time = pygame.time.get_ticks()
    for explosion in explosions[:]:
        pos, frame, start_time = explosion
        if current_time - start_time >= 20:  # Move to the next frame every 20 ms
            frame += 1
            start_time = current_time
        if frame >= len(explosion_frames):
            explosions.remove(explosion)  # Remove explosion after last frame
        else:
            screen.blit(explosion_frames[frame], pos)
            explosion[1] = frame
            explosion[2] = start_time

    # TODO 7: Draw the player's health and score on the screen
    # create a score variable using game_font.render. see pygame dox at https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
    # create a health variable using game_font.render 
    # blit score and health to the top left of the screen


    # Update the display
    pygame.display.flip()

pygame.quit()