# game/ball.py
import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, speed_x=6):
        self.original_x = x
        self.original_y = y
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        # start direction random
        self.velocity_x = random.choice([-1, 1]) * speed_x
        self.velocity_y = random.choice([-1, 1]) * (abs(speed_x) * 0.5)
        self.speed_x = speed_x

    def move(self):
        # move ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # top/bottom collision
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            return "wall"
        if self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            return "wall"
        return None

    def check_collision(self, player, ai):
        """
        Robust collision: check overlap after move. If overlapping with a paddle,
        reflect velocity_x and nudge the ball outside the paddle so high-speed
        tunneling is less likely to let it pass-through repeatedly.
        Also adjust velocity_y based on hit position to give more realistic bounce.
        Returns 'paddle' when a paddle hit occurs, else None.
        """
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()):
            # move ball to the right of player paddle and reverse
            self.x = player.rect().right
            self.velocity_x = abs(self.velocity_x)  # ensure moving right
            self._add_spin(player)
            return "paddle"
        elif ball_rect.colliderect(ai.rect()):
            # move ball to the left of ai paddle and reverse
            self.x = ai.rect().left - self.width
            self.velocity_x = -abs(self.velocity_x)  # ensure moving left
            self._add_spin(ai)
            return "paddle"
        return None

    def _add_spin(self, paddle):
        """Change velocity_y proportionally to where the ball hits the paddle."""
        paddle_center = paddle.y + paddle.height / 2
        ball_center = self.y + self.height / 2
        offset = (ball_center - paddle_center) / (paddle.height / 2)  # -1..1
        max_vert = max(3, abs(self.speed_x) * 0.8)
        self.velocity_y = offset * max_vert
        # slightly increase speed after every paddle hit (small acceleration)
        if self.velocity_x > 0:
            self.velocity_x += 0.2
        else:
            self.velocity_x -= 0.2

    def reset(self, direction=None):
        """Reset ball to center. Optionally force direction: 'left' or 'right'."""
        self.x = float(self.original_x)
        self.y = float(self.original_y)
        if direction == "left":
            self.velocity_x = -abs(self.speed_x)
        elif direction == "right":
            self.velocity_x = abs(self.speed_x)
        else:
            self.velocity_x = random.choice([-1, 1]) * self.speed_x
        self.velocity_y = random.choice([-1, 1]) * (abs(self.speed_x) * 0.5)

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
