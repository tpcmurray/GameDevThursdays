import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800  # Set the width of the window
screen_height = 600  # Set the height of the window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Ship Movement")

# Load images
background = pygame.image.load('assets/background.png')
ship = pygame.image.load('assets/ship_single.png')

# Set the initial position of the ship
ship_rect = ship.get_rect(center=(screen_width // 2, screen_height // 2))

# Set up the clock for frame rate control
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    speed = 5
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
    if keys[pygame.K_UP]:
        ship_rect.y -= speed
    if keys[pygame.K_DOWN]:
        ship_rect.y += speed

    screen.blit(background, (0, 0))
    screen.blit(ship, ship_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
