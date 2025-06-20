#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 COSMIC DEFENDER - Epic Space Shooter Game
Created by AndreyVV
Professional 2D Space Shooter with Advanced Features

To run this game:
1. Install Python 3.8+
2. Install pygame: pip install pygame
3. Run: python cosmic_defender_game.py

To build executable:
Windows: pip install cx-freeze && python setup.py build
Android: pip install buildozer && buildozer android debug
"""

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

class CosmicDefender:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🚀 Cosmic Defender - Created by AndreyVV")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER
        
        # Game variables
        self.score = 0
        self.level = 1
        self.lives = 3
        self.health = 100
        self.max_health = 100
        
        # Player
        self.player = {
            'x': SCREEN_WIDTH // 2,
            'y': SCREEN_HEIGHT - 100,
            'width': 60,
            'height': 40,
            'speed': 8
        }
        
        # Game objects
        self.bullets = []
        self.enemies = []
        self.particles = []
        self.power_ups = []
        self.explosions = []
        
        # Timers
        self.enemy_spawn_timer = 0
        self.power_up_timer = 0
        self.shoot_timer = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Background stars
        self.stars = []
        for _ in range(200):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 3.0),
                'brightness': random.randint(100, 255)
            })
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "PLAYING":
                        self.game_state = "PAUSED"
                    elif self.game_state == "PAUSED":
                        self.game_state = "PLAYING"
                    elif self.game_state == "MENU":
                        self.running = False
                
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "MENU":
                        self.start_game()
                    elif self.game_state == "GAME_OVER":
                        self.restart_game()
                    elif self.game_state == "PAUSED":
                        self.game_state = "PLAYING"
                
                elif event.key == pygame.K_r and self.game_state == "GAME_OVER":
                    self.restart_game()
    
    def start_game(self):
        self.game_state = "PLAYING"
        self.score = 0
        self.level = 1
        self.lives = 3
        self.health = self.max_health
        self.bullets.clear()
        self.enemies.clear()
        self.particles.clear()
        self.power_ups.clear()
        self.explosions.clear()
        self.player['x'] = SCREEN_WIDTH // 2
        self.player['y'] = SCREEN_HEIGHT - 100
    
    def restart_game(self):
        self.start_game()
    
    def update(self):
        if self.game_state == "PLAYING":
            self.update_player()
            self.update_bullets()
            self.update_enemies()
            self.update_particles()
            self.update_power_ups()
            self.update_explosions()
            self.update_stars()
            self.spawn_enemies()
            self.spawn_power_ups()
            self.check_collisions()
            
            # Check game over
            if self.health <= 0 or self.lives <= 0:
                self.game_state = "GAME_OVER"
    
    def update_player(self):
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player['x'] = max(0, self.player['x'] - self.player['speed'])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player['x'] = min(SCREEN_WIDTH - self.player['width'], 
                                 self.player['x'] + self.player['speed'])
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player['y'] = max(0, self.player['y'] - self.player['speed'])
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player['y'] = min(SCREEN_HEIGHT - self.player['height'], 
                                 self.player['y'] + self.player['speed'])
        
        # Shooting
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot_bullet()
            self.shoot_timer = 10
        
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
    
    def shoot_bullet(self):
        bullet = {
            'x': self.player['x'] + self.player['width'] // 2 - 2,
            'y': self.player['y'],
            'width': 4,
            'height': 15,
            'speed': 12,
            'damage': 25,
            'enemy': False
        }
        self.bullets.append(bullet)
        
        # Create muzzle flash particles
        for _ in range(8):
            self.create_particle(bullet['x'], bullet['y'], YELLOW, 2)
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            if bullet['enemy']:
                bullet['y'] += bullet['speed']
                if bullet['y'] > SCREEN_HEIGHT:
                    self.bullets.remove(bullet)
            else:
                bullet['y'] -= bullet['speed']
                if bullet['y'] < -bullet['height']:
                    self.bullets.remove(bullet)
    
    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        spawn_rate = max(30 - self.level * 2, 15)
        
        if self.enemy_spawn_timer >= spawn_rate:
            self.enemy_spawn_timer = 0
            
            enemy_type = random.choice(['basic', 'fast', 'tank', 'zigzag'])
            
            enemy = {
                'x': random.randint(0, SCREEN_WIDTH - 40),
                'y': -40,
                'width': 40,
                'height': 30,
                'speed': random.uniform(2, 4) + self.level * 0.3,
                'health': 50 + self.level * 10,
                'max_health': 50 + self.level * 10,
                'type': enemy_type,
                'direction': 1,
                'shoot_timer': random.randint(60, 120)
            }
            
            # Customize enemy based on type
            if enemy_type == 'fast':
                enemy['speed'] *= 1.5
                enemy['health'] //= 2
                enemy['max_health'] //= 2
            elif enemy_type == 'tank':
                enemy['speed'] *= 0.7
                enemy['health'] *= 2
                enemy['max_health'] *= 2
                enemy['width'] = 50
                enemy['height'] = 40
            
            self.enemies.append(enemy)
    
    def update_enemies(self):
        for enemy in self.enemies[:]:
            # Movement based on type
            if enemy['type'] == 'zigzag':
                enemy['x'] += enemy['direction'] * 3
                if enemy['x'] <= 0 or enemy['x'] >= SCREEN_WIDTH - enemy['width']:
                    enemy['direction'] *= -1
            
            enemy['y'] += enemy['speed']
            
            # Enemy shooting
            enemy['shoot_timer'] -= 1
            if enemy['shoot_timer'] <= 0 and random.random() < 0.02:
                self.enemy_shoot(enemy)
                enemy['shoot_timer'] = random.randint(60, 120)
            
            # Remove enemies that go off screen
            if enemy['y'] > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.health -= 10
    
    def enemy_shoot(self, enemy):
        bullet = {
            'x': enemy['x'] + enemy['width'] // 2 - 2,
            'y': enemy['y'] + enemy['height'],
            'width': 4,
            'height': 10,
            'speed': 6,
            'damage': 15,
            'enemy': True
        }
        self.bullets.append(bullet)
    
    def spawn_power_ups(self):
        self.power_up_timer += 1
        if self.power_up_timer >= 600:  # Every 10 seconds
            self.power_up_timer = 0
            
            power_up_type = random.choice(['health', 'score', 'weapon', 'shield'])
            
            power_up = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': -30,
                'width': 25,
                'height': 25,
                'speed': 3,
                'type': power_up_type,
                'pulse': 0
            }
            self.power_ups.append(power_up)
    
    def update_power_ups(self):
        for power_up in self.power_ups[:]:
            power_up['y'] += power_up['speed']
            power_up['pulse'] += 0.2
            
            if power_up['y'] > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)
    
    def check_collisions(self):
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            if bullet['enemy']:
                continue
                
            for enemy in self.enemies[:]:
                if self.check_collision(bullet, enemy):
                    enemy['health'] -= bullet['damage']
                    self.bullets.remove(bullet)
                    
                    # Create hit particles
                    for _ in range(10):
                        self.create_particle(enemy['x'] + enemy['width']//2, 
                                           enemy['y'] + enemy['height']//2, 
                                           RED, 3)
                    
                    if enemy['health'] <= 0:
                        self.enemies.remove(enemy)
                        self.score += 100 * self.level
                        
                        # Level up every 2000 points
                        if self.score // 2000 > self.level - 1:
                            self.level += 1
                        
                        # Create explosion
                        self.create_explosion(enemy['x'] + enemy['width']//2, 
                                            enemy['y'] + enemy['height']//2)
                    break
        
        # Enemy bullets vs player
        for bullet in self.bullets[:]:
            if not bullet['enemy']:
                continue
                
            if self.check_collision(bullet, self.player):
                self.bullets.remove(bullet)
                self.health -= bullet['damage']
                
                # Create damage particles
                for _ in range(15):
                    self.create_particle(self.player['x'] + self.player['width']//2,
                                       self.player['y'] + self.player['height']//2,
                                       RED, 4)
        
        # Player vs enemies
        for enemy in self.enemies[:]:
            if self.check_collision(self.player, enemy):
                self.enemies.remove(enemy)
                self.health -= 30
                self.lives -= 1
                
                # Create collision explosion
                self.create_explosion(enemy['x'] + enemy['width']//2,
                                    enemy['y'] + enemy['height']//2)
        
        # Player vs power-ups
        for power_up in self.power_ups[:]:
            if self.check_collision(self.player, power_up):
                self.power_ups.remove(power_up)
                
                if power_up['type'] == 'health':
                    self.health = min(self.max_health, self.health + 30)
                elif power_up['type'] == 'score':
                    self.score += 500
                elif power_up['type'] == 'weapon':
                    pass  # Multi-shot for next 10 shots
                elif power_up['type'] == 'shield':
                    self.health = min(self.max_health, self.health + 50)
                
                # Create pickup particles
                for _ in range(12):
                    self.create_particle(power_up['x'] + power_up['width']//2,
                                       power_up['y'] + power_up['height']//2,
                                       GREEN, 2)
    
    def check_collision(self, rect1, rect2):
        return (rect1['x'] < rect2['x'] + rect2['width'] and
                rect1['x'] + rect1['width'] > rect2['x'] and
                rect1['y'] < rect2['y'] + rect2['height'] and
                rect1['y'] + rect1['height'] > rect2['y'])
    
    def create_particle(self, x, y, color, size):
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-5, 5),
            'vy': random.uniform(-5, 5),
            'life': 1.0,
            'decay': random.uniform(0.02, 0.05),
            'color': color,
            'size': size
        }
        self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= particle['decay']
            particle['vy'] += 0.2  # Gravity
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def create_explosion(self, x, y):
        explosion = {
            'x': x,
            'y': y,
            'radius': 5,
            'max_radius': 50,
            'life': 1.0,
            'decay': 0.05
        }
        self.explosions.append(explosion)
        
        # Create explosion particles
        for _ in range(20):
            self.create_particle(x, y, ORANGE, random.randint(2, 5))
    
    def update_explosions(self):
        for explosion in self.explosions[:]:
            explosion['radius'] += 2
            explosion['life'] -= explosion['decay']
            
            if explosion['life'] <= 0 or explosion['radius'] >= explosion['max_radius']:
                self.explosions.remove(explosion)
    
    def update_stars(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = -5
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self):
        # Clear screen with gradient background
        for y in range(SCREEN_HEIGHT):
            color_intensity = int(20 * (1 - y / SCREEN_HEIGHT))
            color = (color_intensity, color_intensity // 2, color_intensity * 2)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, 
                             (int(star['x']), int(star['y'])), 1)
        
        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "PLAYING":
            self.draw_game()
        elif self.game_state == "PAUSED":
            self.draw_game()
            self.draw_pause()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
    
    def draw_menu(self):
        # Title
        title = self.font_large.render("🚀 COSMIC DEFENDER", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Epic Space Shooter Game", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 80))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        instructions = [
            "WASD or Arrow Keys - Move",
            "SPACE - Shoot",
            "ESC - Pause",
            "",
            "Press SPACE to Start!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Credits
        credits = self.font_small.render("Created by AndreyVV", True, YELLOW)
        credits_rect = credits.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(credits, credits_rect)
    
    def draw_game(self):
        # Draw player
        pygame.draw.rect(self.screen, CYAN,
                        (self.player['x'], self.player['y'], 
                         self.player['width'], self.player['height']))
        
        # Draw player details
        pygame.draw.polygon(self.screen, WHITE, [
            (self.player['x'] + self.player['width']//2, self.player['y']),
            (self.player['x'] + 10, self.player['y'] + 20),
            (self.player['x'] + self.player['width'] - 10, self.player['y'] + 20)
        ])
        
        # Draw bullets
        for bullet in self.bullets:
            color = RED if bullet['enemy'] else YELLOW
            pygame.draw.rect(self.screen, color,
                           (bullet['x'], bullet['y'], bullet['width'], bullet['height']))
            if not bullet['enemy']:
                pygame.draw.rect(self.screen, WHITE,
                               (bullet['x']+1, bullet['y'], bullet['width']-2, bullet['height']//2))
        
        # Draw enemies
        for enemy in self.enemies:
            color = RED
            if enemy['type'] == 'fast':
                color = ORANGE
            elif enemy['type'] == 'tank':
                color = (128, 0, 128)
            elif enemy['type'] == 'zigzag':
                color = MAGENTA
                
            pygame.draw.rect(self.screen, color,
                           (enemy['x'], enemy['y'], enemy['width'], enemy['height']))
            
            # Draw health bar
            health_percent = enemy['health'] / enemy['max_health']
            bar_width = enemy['width']
            bar_height = 4
            
            pygame.draw.rect(self.screen, RED,
                           (enemy['x'], enemy['y'] - 8, bar_width, bar_height))
            pygame.draw.rect(self.screen, GREEN,
                           (enemy['x'], enemy['y'] - 8, bar_width * health_percent, bar_height))
        
        # Draw power-ups
        for power_up in self.power_ups:
            pulse = abs(math.sin(power_up['pulse'])) * 0.3 + 0.7
            color = GREEN
            if power_up['type'] == 'score':
                color = YELLOW
            elif power_up['type'] == 'weapon':
                color = CYAN
            elif power_up['type'] == 'shield':
                color = BLUE
                
            color = tuple(int(c * pulse) for c in color)
            pygame.draw.rect(self.screen, color,
                           (power_up['x'], power_up['y'], power_up['width'], power_up['height']))
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))
        
        # Draw explosions
        for explosion in self.explosions:
            color = (255, int(165 * explosion['life']), 0)
            pygame.draw.circle(self.screen, color,
                             (int(explosion['x']), int(explosion['y'])),
                             int(explosion['radius']), 3)
        
        # Draw UI
        self.draw_ui()
    
    def draw_ui(self):
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (20, 60))
        
        # Lives
        lives_text = self.font_medium.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 100))
        
        # Health bar
        bar_width = 200
        bar_height = 20
        health_percent = self.health / self.max_health
        
        pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH - bar_width - 20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - bar_width - 20, 20, bar_width * health_percent, bar_height))
        
        health_text = self.font_small.render(f"Health: {self.health}/{self.max_health}", True, WHITE)
        self.screen.blit(health_text, (SCREEN_WIDTH - bar_width - 20, 45))
    
    def draw_pause(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, CYAN)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        resume_text = self.font_medium.render("Press ESC or SPACE to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Level reached
        level_text = self.font_medium.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(level_text, level_rect)
        
        # Restart instructions
        restart_text = self.font_medium.render("Press SPACE or R to Play Again", True, CYAN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        # Credits
        credits = self.font_small.render("Created by AndreyVV", True, YELLOW)
        credits_rect = credits.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(credits, credits_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to run the game"""
    try:
        print("🚀 Starting Cosmic Defender...")
        print("Created by AndreyVV")
        print("Controls: WASD/Arrow Keys to move, SPACE to shoot, ESC to pause")
        game = CosmicDefender()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
