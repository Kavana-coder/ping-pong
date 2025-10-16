# main.py
import pygame
from game.game_engine import GameEngine

def main():
    pygame.init()
    pygame.mixer.init()  # initialize mixer (safe even if no sounds present)
    WIDTH, HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong - Pygame Version")
    clock = pygame.time.Clock()
    FPS = 60

    engine = GameEngine(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # pass events to engine so it can handle e.g. menu keypresses
            engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
