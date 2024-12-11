
import pygame
import os

class Beam:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle
        self.direction = pygame.math.Vector2(0, -1).rotate(angle)
        self.beam_image = pygame.image.load(os.path.join("assets", "beam.png")).convert_alpha()

    def move(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self, surface):
        surface.blit(self.beam_image, (self.x, self.y))