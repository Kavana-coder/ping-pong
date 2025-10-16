# game/game_engine.py
import pygame
import os
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")

class GameEngine:
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    STATE_MENU = "menu"

    def __init__(self, width, height, winning_score=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Create paddles and ball
        self.player = Paddle(10, height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height, speed=9)
        self.ai = Paddle(width - 20, height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height, speed=7)
        self.ball = Ball(width // 2 - 4, height // 2 - 4, 8, 8, width, height, speed_x=6)

        # scores and fonts
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = winning_score
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)

        # state
        self.state = GameEngine.STATE_PLAYING

        # sounds (optional)
        self.sound_paddle = None
        self.sound_wall = None
        self.sound_score = None
        self._load_sounds()

    def _safe_load_sound(self, filename):
        try:
            path = os.path.join(ASSETS_DIR, filename)
            if not os.path.exists(path):
                return None
            return pygame.mixer.Sound(path)
        except Exception:
            return None

    def _load_sounds(self):
        # Expected place: project/assets/sounds/paddle.wav etc.
        self.sound_paddle = self._safe_load_sound("paddle.wav")
        self.sound_wall = self._safe_load_sound("wall.wav")
        self.sound_score = self._safe_load_sound("score.wav")

    def handle_event(self, event):
        """Handle events for menus / replay choices."""
        if self.state == GameEngine.STATE_GAME_OVER and event.type == pygame.KEYDOWN:
            # 3 / 5 / 7 or ESC to quit
            if event.key == pygame.K_3:
                self._start_new_match(3)
            elif event.key == pygame.K_5:
                self._start_new_match(5)
            elif event.key == pygame.K_7:
                self._start_new_match(7)
            elif event.key == pygame.K_ESCAPE:
                # quit pygame loop by posting QUIT event
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_input(self):
        if self.state != GameEngine.STATE_PLAYING:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)

    def update(self):
        if self.state != GameEngine.STATE_PLAYING:
            return

        wall_hit = self.ball.move()
        if wall_hit == "wall" and self.sound_wall:
            self.sound_wall.play()
        paddle_hit = self.ball.check_collision(self.player, self.ai)
        if paddle_hit == "paddle" and self.sound_paddle:
            self.sound_paddle.play()

        # score checks (left or right out)
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.sound_score:
                self.sound_score.play()
            # reset toward player (ball moves right)
            self.ball.reset(direction="right")
            self._check_game_over()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            if self.sound_score:
                self.sound_score.play()
            # reset toward ai (ball moves left)
            self.ball.reset(direction="left")
            self._check_game_over()

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

    def _check_game_over(self):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.state = GameEngine.STATE_GAME_OVER

    def _start_new_match(self, winning_score):
        """Reset scores and ball to start a new match with chosen winning score."""
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.state = GameEngine.STATE_PLAYING

    def render(self, screen):
        # clear
        screen.fill(BLACK)

        # center line
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
        screen.blit(ai_text, (self.width*3//4 - ai_text.get_width()//2, 20))

        # show instructions
        instr = self.small_font.render("W/S = Move | First to {} wins".format(self.winning_score), True, WHITE)
        screen.blit(instr, (10, self.height - 30))

        # game over screen / menu
        if self.state == GameEngine.STATE_GAME_OVER:
            winner = "Player" if self.player_score > self.ai_score else "AI"
            overlay = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))

            title = self.font.render(f"{winner} Wins!", True, WHITE)
            screen.blit(title, (self.width//2 - title.get_width()//2, self.height//2 - 80))

            msg = self.small_font.render("Press 3 (Best of 3), 5 (Best of 5), 7 (Best of 7) to replay, ESC to exit", True, WHITE)
            screen.blit(msg, (self.width//2 - msg.get_width()//2, self.height//2))

            score_detail = self.small_font.render(f"Final Score — Player: {self.player_score}   AI: {self.ai_score}", True, WHITE)
            screen.blit(score_detail, (self.width//2 - score_detail.get_width()//2, self.height//2 + 40))
