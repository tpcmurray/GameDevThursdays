import pygame
import os

class Background:
    def __init__(self, screen_height):
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()
        self.y1 = 0
        self.y2 = -self.background_image.get_height()
        self.speed = 1
        self.screen_height = screen_height  # Store screen height
    
    def move(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= self.screen_height:
            self.y1 = self.y2 - self.background_image.get_height()
        if self.y2 >= self.screen_height:
            self.y2 = self.y1 - self.background_image.get_height()
    
    def draw(self, surface):
        surface.blit(self.background_image, (0, self.y1))
        surface.blit(self.background_image, (0, self.y2))