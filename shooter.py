import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 700  # Set the width of the window
screen_height = 1000  # Set the height of the window
screen = pygame.display.set_mode((screen_width, screen_height))

# load, play, and loop music at 50% volume
# TODO 1 load music
# TODO 1 set volume to 50%
# TODO 1 loop infinitely 

# TODO 2 comment out the below line and work on the lines below
ship = pygame.image.load('assets/ship_single.png') 
# load ship sprite sheet, load 3 ship images. the image is 192 x 64. all images are 64x64
# TODO 2 load ship image, and use convert_alpha
# TODO 2 create ship_left  (how big is the image? each ship is one third of the image size)
#      use ship.subsurface to get the left ship
# TODO 2 create ship_center
# TODO 2 create ship_right

# TODO 2 when do we switch the ship graphics?
ship_rect = ship.get_rect(center=(screen_width // 2, screen_height  - 50))

# Load background
background = pygame.image.load('assets/background.png')
# TODO 3 track the backgrounds y location

# variables
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        ship_rect.x += speed
    if keys[pygame.K_UP]:
        ship_rect.y -= speed
    if keys[pygame.K_DOWN]:
        ship_rect.y += speed

    # TODO 3 scroll the background before drawing it, along the y axis

    # TODO 3 the below line needs to change, and you need another like it for the 2nd copy
    screen.blit(background, (0, 0))
    screen.blit(ship, ship_rect)
    pygame.display.flip()

pygame.quit()
