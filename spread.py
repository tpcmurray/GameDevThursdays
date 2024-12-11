
import pygame
import os

class Spread:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # Move very slowly towards the player
        self.spread_image = pygame.image.load(os.path.join("assets", "spread.png")).convert_alpha()

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.spread_image, (self.x, self.y))