import pygame
import os
import random

class Projectile:
    beam_image = None
    bullet_image = None
    laser_sounds = None
    
    def __init__(self, x, y, is_beam=True):
        if Projectile.beam_image is None:
            Projectile.beam_image = pygame.image.load(os.path.join("assets", "beam.png")).convert_alpha()
            Projectile.bullet_image = pygame.image.load(os.path.join("assets", "projectile.png")).convert_alpha()
            Projectile.laser_sounds = [
                pygame.mixer.Sound(os.path.join("assets", "laser1.mp3")),
                pygame.mixer.Sound(os.path.join("assets", "laser2.mp3")),
                pygame.mixer.Sound(os.path.join("assets", "laser3.mp3"))
            ]
        
        self.is_beam = is_beam
        self.image = Projectile.beam_image if is_beam else Projectile.bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = -5 if is_beam else 0  # Beams always move up
        
    def set_direction(self, target_x, target_y):
        if not self.is_beam:
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            length = (dx * dx + dy * dy) ** 0.5
            if length > 0:
                self.dx = dx / length * 3
                self.dy = dy / length * 3
    
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
    
    @staticmethod
    def play_laser_sound():
        random.choice(Projectile.laser_sounds).play()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)