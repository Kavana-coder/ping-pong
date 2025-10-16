import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize pygame mixer for sound
        pygame.mixer.init()

        # Load sound for end game
        self.end_game_sound = pygame.mixer.Sound("game/end-game.mp3")

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.target_score = 5   # 🔥 new: winning score (default 5)

    def reset_game(self):
        """Resets scores and ball for a new match."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()

    def check_game_over(self, screen):
        if self.player_score == self.target_score:
            winner_text = self.font.render("Player Wins!", True, (255, 255, 255))
            screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2,
                                      self.height//2 - winner_text.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(1500)

            # 🔊 Play end-game sound
            self.end_game_sound.play()

            self.show_replay_menu(screen)
            return True

        elif self.ai_score == self.target_score:
            winner_text = self.font.render("AI Wins!", True, (255, 255, 255))
            screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2,
                                      self.height//2 - winner_text.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(1500)

            # 🔊 Play end-game sound
            self.end_game_sound.play()

            self.show_replay_menu(screen)
            return True

        return False

    def show_replay_menu(self, screen):
        """Displays replay options and waits for user input."""
        menu_font = pygame.font.SysFont("Arial", 28)
        options = [
            "Replay (Press Enter)",      # 🔥 Added replay option
            "Best of 3 (Press 3)",
            "Best of 5 (Press 5)",
            "Best of 7 (Press 7)",
            "Exit (Press ESC)"
        ]

        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            y_offset = self.height // 2 - 50
            for opt in options:
                text = menu_font.render(opt, True, (255, 255, 255))
                screen.blit(text, (self.width//2 - text.get_width()//2, y_offset))
                y_offset += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:   # 🔥 Replay pressed
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_3:
                        self.target_score = 2   # Best of 3 → first to 2
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.target_score = 3   # Best of 5 → first to 3
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.target_score = 4   # Best of 7 → first to 4
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move ball first
        self.ball.move()

        # Check for collisions with paddles
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.velocity_x = abs(self.ball.velocity_x)  # ensure ball goes right
        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.velocity_x = -abs(self.ball.velocity_x)  # ensure ball goes left

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Update AI paddle movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
