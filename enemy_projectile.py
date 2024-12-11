
import pygame
import os
import random

class EnemyProjectile:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5
        self.angle = 0  # Initial angle for spinning
        self.enemy_projectile_image = pygame.image.load(os.path.join("assets", "projectile.png")).convert_alpha()

        # Calculate direction vector
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        self.direction = direction.normalize()

    def move(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        self.angle += 10  # Spin the projectile

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.enemy_projectile_image, self.angle)
        surface.blit(rotated_image, (self.x, self.y))