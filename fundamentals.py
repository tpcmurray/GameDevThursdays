import pygame

pygame.init()

screen_width = 800
screen_height = 600
red = (255, 0, 0)
green = (0, 255, 0)
screen = pygame.display.set_mode((screen_width, screen_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        screen.fill(red)
    else:
        screen.fill(green)

    pygame.display.flip()

pygame.quit()

