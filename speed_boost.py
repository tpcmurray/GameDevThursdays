
import pygame
import os

class SpeedBoost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # Move very slowly towards the player
        self.speed_boost_image = pygame.image.load(os.path.join("assets", "speed.png")).convert_alpha()

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.speed_boost_image, (self.x, self.y))