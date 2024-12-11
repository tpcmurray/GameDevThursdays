import pygame
import os

# Import classes from their modules
from beam import Beam
from enemy_projectile import EnemyProjectile
from enemy import Enemy
from background import Background
from speed_boost import SpeedBoost
from spread import Spread
from player import Player

# Initialize Pygame
pygame.init()

# Load background music
pygame.mixer.music.load(os.path.join("assets", "backtrack.mp3"))
pygame.mixer.music.set_volume(0.5)  # Set volume to 70% (reduce by 30%)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Remove RESIZABLE flag
pygame.display.set_caption("Ship Game")

# Colors
BLACK = (0, 0, 0)

# Load and split the ship sprite sheet
# Assuming ship.png is in the assets folder
sprite_sheet = pygame.image.load(os.path.join("assets", "ship.png")).convert_alpha()
sprite_width = sprite_sheet.get_width() // 3  # Divide by 3 since there are 3 frames
sprite_height = sprite_sheet.get_height()

# Load laser sound files
laser_sounds = [
    pygame.mixer.Sound(os.path.join("assets", "laser1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "laser2.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "laser3.mp3"))
]

# Load enemy image
enemy_image = pygame.image.load(os.path.join("assets", "enemy1.png")).convert_alpha()

# Load enemy projectile image
enemy_projectile_image = pygame.image.load(os.path.join("assets", "projectile.png")).convert_alpha()

# Load background image
background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

# Load font
font = pygame.font.Font(os.path.join("assets", "font.ttf"), 32)

# Load logo image
logo_image = pygame.image.load(os.path.join("assets", "space-shooter-logo.png")).convert_alpha()

# Load and split the explosion sprite sheet
explosion_sheet = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
explosion_frames = []
for i in range(5):
    frame = explosion_sheet.subsurface((i * 128, 0, 128, 128))
    explosion_frames.append(frame)


# Create surfaces for each ship state
ship_left = sprite_sheet.subsurface((0, 0, sprite_width, sprite_height))
ship_center = sprite_sheet.subsurface((sprite_width, 0, sprite_width, sprite_height))
ship_right = sprite_sheet.subsurface((sprite_width * 2, 0, sprite_width, sprite_height))

# Constants for power-up thresholds
SPEED_BOOST_THRESHOLD = 100
SPREAD_THRESHOLD = 289

def show_game_over_screen(surface, score):
    surface.fill(BLACK)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()

def show_start_screen(surface):
    surface.fill(BLACK)
    start_text = font.render("Press any key to start", True, (255, 255, 255))
    # Center the logo at the same vertical position as before
    surface.blit(logo_image, (SCREEN_WIDTH // 2 - logo_image.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    surface.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def game_over():
    show_game_over_screen(screen, player.score)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    global player, background, running, global_timer
    player = Player(
        x=SCREEN_WIDTH // 2,
        y=SCREEN_HEIGHT - 100,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        enemy_image=enemy_image,
        enemy_projectile_image=enemy_projectile_image,
        explosion_frames=explosion_frames,
        game_over_callback=game_over
    )
    background = Background(SCREEN_HEIGHT)  # Pass SCREEN_HEIGHT
    running = True
    clock = pygame.time.Clock()
    global_timer = 0  # Initialize global timer

    show_start_screen(screen)  # Show start screen before the game loop

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Update player
        player.move(keys)
        player.update_beams()
        player.update_enemies(global_timer)
        player.update_spreads()
        background.move()
        
        # Draw
        screen.fill(BLACK)
        background.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
        global_timer += 1  # Increment global timer
        
        if player.lives <= 0:
            running = False
            game_over()

if __name__ == "__main__":
    main()
    pygame.quit()