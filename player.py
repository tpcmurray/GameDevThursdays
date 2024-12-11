import random
import pygame
import os
from beam import Beam
from enemy import Enemy
from speed_boost import SpeedBoost
from spread import Spread

class Player:
    def __init__(self, x, y, screen_width, screen_height, enemy_image, enemy_projectile_image, 
                 explosion_frames, game_over_callback):
        self.x = x
        self.y = y
        self.speed = 5
        # Screen dimensions
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        # Game assets and images
        self.enemy_image = enemy_image
        self.enemy_projectile_image = enemy_projectile_image
        self.explosion_frames = explosion_frames
        self.game_over_callback = game_over_callback
        # Load and split the ship sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.join("assets", "ship.png")).convert_alpha()
        self.sprite_width = self.sprite_sheet.get_width() // 3  # Divide by 3 since there are 3 frames
        self.sprite_height = self.sprite_sheet.get_height()
        # Load beam image
        self.beam_image = pygame.image.load(os.path.join("assets", "beam.png")).convert_alpha()
        # Load speed boost image
        self.speed_boost_image = pygame.image.load(os.path.join("assets", "speed.png")).convert_alpha()
        # Load spread image
        self.spread_image = pygame.image.load(os.path.join("assets", "spread.png")).convert_alpha()
        # Load laser sound files
        self.laser_sounds = [
            pygame.mixer.Sound(os.path.join("assets", "laser1.mp3")),
            pygame.mixer.Sound(os.path.join("assets", "laser2.mp3")),
            pygame.mixer.Sound(os.path.join("assets", "laser3.mp3"))
        ]
        # Load font
        self.font = pygame.font.Font(os.path.join("assets", "font.ttf"), 32)
        # Create surfaces for each ship state
        self.ship_left = self.sprite_sheet.subsurface((0, 0, self.sprite_width, self.sprite_height))
        self.ship_center = self.sprite_sheet.subsurface((self.sprite_width, 0, self.sprite_width, self.sprite_height))
        self.ship_right = self.sprite_sheet.subsurface((self.sprite_width * 2, 0, self.sprite_width, self.sprite_height))
        # Constants for power-up thresholds
        self.SPEED_BOOST_THRESHOLD = 100
        self.SPREAD_THRESHOLD = 289
        # Update current_image to use self.ship_center
        self.current_image = self.ship_center
        self.beams = []
        self.enemies = []
        self.spawn_initial_enemies()
        self.score = 0
        self.lives = 3  # Add lives attribute
        self.enemy_projectiles = []  # Manage all enemy projectiles here
        self.speed_boosts = []
        self.spreads = []
        self.enemies_killed = 0  # Track number of enemies killed
        self.has_spread = False  # Track if player has picked up spread power-up
        self.hit_timer = 0  # Timer for blinking effect
        
    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.current_image = self.ship_left
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.current_image = self.ship_right
        else:
            self.current_image = self.ship_center
            
        # Keep player on screen
        self.x = max(0, min(self.x, self.SCREEN_WIDTH - self.sprite_width))
        self.y = max(0, min(self.y, self.SCREEN_HEIGHT - self.sprite_height))
    
    def shoot(self):
        beam_x = self.x + (self.sprite_width // 2) - (self.beam_image.get_width() // 2)
        beam_y = self.y
        self.beams.append(Beam(beam_x, beam_y))
        if self.has_spread:
            self.beams.append(Beam(self.x, self.y, -20))  # Left angled beam
            self.beams.append(Beam(self.x + self.sprite_width, self.y, 20))  # Right angled beam
        random.choice(self.laser_sounds).play()
    
    def update_beams(self):
        for beam in self.beams:
            beam.move()
            if beam.y < 0:
                self.beams.remove(beam)
            else:
                for enemy in self.enemies:
                    if self.check_collision(beam, enemy):
                        self.beams.remove(beam)
                        if not enemy.exploding:
                            # Start explosion animation
                            enemy.exploding = True
                            enemy.current_explosion_frame = 0
                            enemy.explosion_timer = 0
                            # Spawn a new enemy
                            self.spawn_enemy()
                        self.score += 100
                        self.enemies_killed += 1  # Increment enemies killed
                        if self.enemies_killed % self.SPEED_BOOST_THRESHOLD == 0:  # Every 100 enemies killed
                            self.spawn_speed_boost(enemy.x, enemy.y)
                        if self.enemies_killed == self.SPREAD_THRESHOLD:  
                            self.spawn_spread(enemy.x, enemy.y)
                        break
        self.update_enemy_projectiles()
        self.update_speed_boosts()
        self.update_spreads()  # Ensure this is called

    def spawn_speed_boost(self, x, y):
        self.speed_boosts.append(SpeedBoost(x, y))

    def spawn_spread(self, x, y):
        self.spreads.append(Spread(x, y))

    def update_speed_boosts(self):
        for boost in self.speed_boosts:
            boost.move()
            if self.check_collision_with_boost(boost):
                self.speed_boosts.remove(boost)
                self.speed = int(self.speed * 1.3)  # Increase speed by 30%

    def update_spreads(self):
        for spread in self.spreads:
            spread.move()
            if self.check_collision_with_spread(spread):
                self.spreads.remove(spread)
                self.has_spread = True  # Activate spread power-up

    def check_collision_with_boost(self, boost):
        boost_rect = pygame.Rect(boost.x, boost.y, self.speed_boost_image.get_width(), self.speed_boost_image.get_height())
        player_rect = pygame.Rect(self.x, self.y, self.sprite_width, self.sprite_height)
        return boost_rect.colliderect(player_rect)

    def check_collision_with_spread(self, spread):
        spread_rect = pygame.Rect(spread.x, spread.y, self.spread_image.get_width(), self.spread_image.get_height())
        player_rect = pygame.Rect(self.x, self.y, self.sprite_width, self.sprite_height)
        return spread_rect.colliderect(player_rect)
    
    def check_collision(self, beam, enemy):
        beam_rect = pygame.Rect(beam.x, beam.y, self.beam_image.get_width(), self.beam_image.get_height())
        enemy_rect = pygame.Rect(enemy.x, enemy.y, self.enemy_image.get_width(), self.enemy_image.get_height())
        return beam_rect.colliderect(enemy_rect)
    
    def check_collision_with_projectile(self, projectile):
        projectile_rect = pygame.Rect(projectile.x, projectile.y, self.enemy_projectile_image.get_width(), self.enemy_projectile_image.get_height())
        player_rect = pygame.Rect(self.x, self.y, self.sprite_width, self.sprite_height)
        return projectile_rect.colliderect(player_rect)
    
    def spawn_initial_enemies(self):
        for _ in range(5):  # Spawn 5 enemies initially
            self.spawn_enemy()
    
    def spawn_enemy(self):
        enemy_x = random.randint(0, self.SCREEN_WIDTH - self.enemy_image.get_width())
        enemy_y = random.randint(-100, -40)
        self.enemies.append(
            Enemy(
                enemy_x,
                enemy_y,
                self.explosion_frames,
                self.sprite_width,
                self.sprite_height
            )
        )
    
    def update_enemies(self, global_timer):
        for enemy in self.enemies:
            enemy.move(self, global_timer)
            if enemy.y > self.SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.spawn_enemy()
    
    def update_enemy_projectiles(self):
        for projectile in self.enemy_projectiles:
            projectile.move()
            if self.check_collision_with_projectile(projectile):
                self.enemy_projectiles.remove(projectile)
                self.lives -= 1
                self.hit_timer = 30  # Set hit timer to 30 frames (500 ms at 60 FPS)
                if self.lives <= 0:
                    self.game_over_callback()
    
    def draw(self, surface):
        # Draw all non-player elements first
        for beam in self.beams:
            beam.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface, self)
        for projectile in self.enemy_projectiles:
            projectile.draw(surface)
        for boost in self.speed_boosts:
            boost.draw(surface)
        for spread in self.spreads:
            spread.draw(surface)
        
        # Draw player ship with blinking effect
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer % 10 < 5:  # Blink effect
                self.draw_score(surface)
                self.draw_lives(surface)
                return
        surface.blit(self.current_image, (self.x, self.y))
        
        # Draw UI elements
        self.draw_score(surface)
        self.draw_lives(surface)

    def draw_score(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
    
    def draw_lives(self, surface):
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (10, 50))