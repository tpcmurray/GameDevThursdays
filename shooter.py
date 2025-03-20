import pygame
import os
import random
from pygame.mixer import music
from player import Player
from enemy import Enemy
from projectile import Projectile

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 700
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# load, play, and loop music at 50% volume
music.load(os.path.join("assets", "backtrack.mp3"))
music.set_volume(0.5)
music.play(-1)

# Load explosion image and sound
explosion_img = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
explosion_sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
explosion_frames = [explosion_img.subsurface((i * 128, 0, 128, 128)) for i in range(5)]

# Load background
background = pygame.image.load('assets/background.png')
background1_y = 0
background2_y = -background.get_height()
background_speed = 0.5

# Add font initialization
game_font = pygame.font.Font("assets/font.ttf", 36)

# Create player
player = Player(screen_width, screen_height)

# Initialize game variables
score = 0
enemies = []
beams = []
enemy_bullets = []
explosions = []
count_frames = 0
spawn_enemies_every = 200

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                beam = Projectile(player.rect.centerx, player.rect.top, is_beam=True)
                beams.append(beam)
                Projectile.play_laser_sound()

    # Update the frame counter
    count_frames += 1
    if count_frames > spawn_enemies_every:
        count_frames = 0

    # Move player
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Spawn a new enemy
    if count_frames >= spawn_enemies_every:
        enemy = Enemy(screen_width)
        enemies.append(enemy)
        
        # Random chance for existing enemies to shoot
        for e in enemies:
            if random.random() < 0.5:  # % chance to shoot
                bullet = Projectile(e.rect.centerx, e.rect.bottom, is_beam=False)
                bullet.set_direction(player.rect.centerx, player.rect.centery)
                enemy_bullets.append(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.move(screen_width)
    
    # Move beams
    for beam in beams[:]:
        beam.move()
        if beam.rect.bottom < 0:
            beams.remove(beam)

    # Move enemy bullets
    for bullet in enemy_bullets[:]:
        bullet.move()
        if bullet.rect.colliderect(player.rect):
            enemy_bullets.remove(bullet)
            player.health -= 25
            if player.health <= 0:
                running = False
        elif (bullet.rect.top > screen_height or bullet.rect.bottom < 0 or 
              bullet.rect.left > screen_width or bullet.rect.right < 0):
            enemy_bullets.remove(bullet)

    # Check for collisions between beams and enemies
    for beam in beams[:]:
        for enemy in enemies[:]:
            if beam.rect.colliderect(enemy.rect):
                beams.remove(beam)
                enemies.remove(enemy)
                explosions.append([enemy.rect.topleft, 0, pygame.time.get_ticks()])
                explosion_sound.play()
                score += 100
                break

    # scroll the background
    background1_y += background_speed
    background2_y += background_speed
    if background1_y > screen_height:
        background1_y = -background.get_height()
    if background2_y > screen_height:
        background2_y = -background.get_height()

    # Draw everything
    screen.blit(background, (0, background1_y))
    screen.blit(background, (0, background2_y))
    player.draw(screen)
    
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in enemy_bullets:
        bullet.draw(screen)
    for beam in beams:
        beam.draw(screen)

    # Draw explosions
    current_time = pygame.time.get_ticks()
    for explosion in explosions[:]:
        pos, frame, start_time = explosion
        if current_time - start_time >= 20:
            frame += 1
            start_time = current_time
        if frame >= len(explosion_frames):
            explosions.remove(explosion)
        else:
            screen.blit(explosion_frames[frame], pos)
            explosion[1] = frame
            explosion[2] = start_time
    
    # Draw score and health
    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    health_text = game_font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()

pygame.quit()