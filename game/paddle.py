# game/paddle.py
import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, dy, screen_height):
        """Move paddle vertically while keeping inside screen bounds."""
        self.y += dy
        if self.y < 0:
            self.y = 0
        if self.y + self.height > screen_height:
            self.y = screen_height - self.height

    def auto_track(self, ball, screen_height):
        """
        Simple AI that tracks the ball's vertical position.
        Limits speed to self.speed to keep AI beatable.
        """
        paddle_center = self.y + self.height / 2
        ball_center = ball.y + ball.height / 2
        # small deadzone so AI doesn't jitter
        if abs(ball_center - paddle_center) < 5:
            return
        if ball_center > paddle_center:
            self.move(min(self.speed, ball_center - paddle_center), screen_height)
        else:
            self.move(-min(self.speed, paddle_center - ball_center), screen_height)

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
