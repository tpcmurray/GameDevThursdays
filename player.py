import pygame
import os

class Player:
    def __init__(self, screen_width, screen_height):
        # Load ship sprite sheet, load 3 ship images
        sprite_sheet = pygame.image.load(os.path.join("assets", "ship.png")).convert_alpha()
        sprite_width = sprite_sheet.get_width() // 3
        sprite_height = sprite_sheet.get_height()
        self.ship_left = sprite_sheet.subsurface((0, 0, sprite_width, sprite_height))
        self.ship_center = sprite_sheet.subsurface((sprite_width, 0, sprite_width, sprite_height))
        self.ship_right = sprite_sheet.subsurface((sprite_width * 2, 0, sprite_width, sprite_height))
        self.ship = self.ship_center
        self.rect = self.ship.get_rect(center=(screen_width // 2, screen_height - 50))
        self.health = 100
        self.speed = 2
        
    def move(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.ship = self.ship_left
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.ship = self.ship_right
        else:
            self.ship = self.ship_center
            
    def draw(self, screen):
        screen.blit(self.ship, self.rect)