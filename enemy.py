import pygame
import os
import random

class Enemy:
    image = None
    
    def __init__(self, screen_width):
        if Enemy.image is None:
            Enemy.image = pygame.image.load(os.path.join("assets", "enemy1.png")).convert_alpha()
        self.rect = Enemy.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.x_speed = random.uniform(-2, 2)
        if self.x_speed < .1 and self.x_speed > -.1:
            self.x_speed = .3
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def move(self, screen_width):
        self.x += self.x_speed
        self.y += 1.0 * random.uniform(1, 2)
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.rect.x <= 0 or self.rect.x > screen_width - self.rect.width:
            self.x_speed = -self.x_speed
            
    def draw(self, screen):
        screen.blit(Enemy.image, self.rect)