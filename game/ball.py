import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Initialize sound effects as None - they're optional
        self.sound_paddle = None
        self.sound_wall = None
        self.sound_score = None
        
        # Try to load sound effects if available
        try:
            self.sound_paddle = pygame.mixer.Sound("game/paddle_hit.wav")
            self.sound_wall = pygame.mixer.Sound("game/wall_bounce.wav")
            self.sound_score = pygame.mixer.Sound("game/score.wav")
        except:
            print("Sound files not found - running without sound effects")

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.sound_wall:
                self.sound_wall.play()   # 🔊 Play wall bounce sound

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()  # 🔊 Play paddle hit sound

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if self.sound_score:
            self.sound_score.play()   # 🔊 Play scoring sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
