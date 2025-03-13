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

# Load projectile
projectile_img = pygame.image.load(os.path.join("assets", "projectile.png")).convert_alpha()

# Add font initialization
game_font = pygame.font.Font("assets/font.ttf", 36)

# variables
player_health = 100
speed = 2
score = 0  # Add score variable
enemies = []  # List to store enemies - each enemy will be [rect, x_speed]
beams = []    # List to store active beams
enemy_bullets = []  # List to store enemy bullets [rect, dx, dy]
explosions = []  # List to store active explosions
count_frames = 0
spawn_enemies_every = 200  # Spawn an enemy every so many frames

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
        
        # Random chance for existing enemies to shoot
        for enemy in enemies:
            if random.random() < 0.5:  # % chance to shoot
                bullet = projectile_img.get_rect()
                bullet.centerx = enemy[0].centerx
                bullet.top = enemy[0].bottom
                
                # Calculate direction to player
                dx = ship_rect.centerx - bullet.centerx
                dy = ship_rect.centery - bullet.centery
                # Normalize the direction vector
                length = (dx * dx + dy * dy) ** 0.5
                if length > 0:
                    dx = dx / length * 3  # Speed of 3
                    dy = dy / length * 3
                enemy_bullets.append([bullet, dx, dy])

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

    # Move enemy bullets in their calculated direction
    for bullet in enemy_bullets[:]:
        bullet[0].x += bullet[1]  # Move by dx
        bullet[0].y += bullet[2]  # Move by dy

        # Check if bullet hits player
        if bullet[0].colliderect(ship_rect):
            enemy_bullets.remove(bullet)
            player_health -= 25
            if player_health <= 0:
                running = False
        elif bullet[0].top > screen_height or bullet[0].bottom < 0 or bullet[0].left > screen_width or bullet[0].right < 0:
            enemy_bullets.remove(bullet)

    # Check for collisions between beams and enemies
    for beam in beams[:]:
        for enemy in enemies[:]:
            if beam.colliderect(enemy[0]):
                beams.remove(beam)
                enemies.remove(enemy)
                explosions.append([enemy[0].topleft, 0, pygame.time.get_ticks()])  # Add explosion at enemy position
                explosion_sound.play()
                score += 100  # Add score when enemy is destroyed
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
        
    # Draw all enemy bullets
    for bullet in enemy_bullets:
        screen.blit(projectile_img, bullet[0])
        
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
    
    # Draw score and health
    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    health_text = game_font.render(f"Health: {player_health}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    # Update the display
    pygame.display.flip()

pygame.quit()