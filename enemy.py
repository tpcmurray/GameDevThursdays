import pygame
import os
import random
from enemy_projectile import EnemyProjectile
# from player import player, global_timer, SCREEN_WIDTH, enemy_image

class Enemy:
    def __init__(self, x, y, explosion_frames, sprite_width, sprite_height):
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(1, 3)
        self.fire_timer = random.randint(100, 200)  # Initial fire timer
        self.exploding = False
        self.explosion_frames = explosion_frames
        self.current_explosion_frame = 0
        self.explosion_timer = 0  # Timer to control explosion frame rate
        self.explosion_sound_played = False  # Flag to check if sound has been played
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.explosion_sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
        self.explosion_sound.set_volume(0.2)
    
    def move(self, player, global_timer):
        if not self.exploding:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.x < 0 or self.x > player.SCREEN_WIDTH - player.enemy_image.get_width():
                self.speed_x = -self.speed_x
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.fire_projectile(player)
                self.fire_timer = max(50, 200 - global_timer // 10)  # Decrease fire timer based on global timer
        else:
            if not self.explosion_sound_played:
                self.explosion_sound.play()
                self.explosion_sound_played = True
            # Update explosion animation
            self.explosion_timer += 1
            if self.explosion_timer % 5 == 0:  # Adjust speed of animation if needed
                self.current_explosion_frame += 1
                if self.current_explosion_frame >= len(self.explosion_frames):
                    # Remove enemy after explosion animation completes
                    player.enemies.remove(self)
    
    def fire_projectile(self, player):
        target_x = player.x + self.sprite_width // 2
        target_y = player.y + self.sprite_height // 2
        player.enemy_projectiles.append(EnemyProjectile(self.x, self.y, target_x, target_y))
    
    def draw(self, surface, player):
        if not self.exploding:
            surface.blit(player.enemy_image, (self.x, self.y))
        else:
            # Draw explosion frame centered on enemy position
            frame = self.explosion_frames[self.current_explosion_frame]
            frame_rect = frame.get_rect(center=(self.x + player.enemy_image.get_width() // 2, self.y + player.enemy_image.get_height() // 2))
            surface.blit(frame, frame_rect)