import pygame
from time import time
from sys import exit
from resources import FPS
from game import Game
from traceback import print_exc

pygame.init()
clock = pygame.time.Clock()

if __name__ == "__main__":
    try:
        game = Game()

        frame_count = 0
        start_time = time()

        while game.running:
            game.run()
            pygame.display.flip()
            clock.tick(FPS)

            # frame_count += 1
            # if (time.time() - start_time) > 1:  # cada segundo
            #     fps = frame_count / (time() - start_time)
            #     print(f"FPS: {fps}")
            #     frame_count = 0
            #     start_time = time()

        pygame.quit()
        exit(0)

    except Exception as error:
        print("Error:", error)
        print_exc()
        pygame.quit()
        exit(1)
