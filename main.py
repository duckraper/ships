import pygame
from time import time
from sys import exit
from resources import FPS, joysticks
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                    break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.running = False
                        break

                    if event.key == pygame.K_p:
                        game.toggle_pause()
                
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        game.toggle_pause()

                if event.type == pygame.JOYDEVICEADDED:
                    joysticks.append(pygame.joystick.Joystick(event.device_index))
                    joy_count = pygame.joystick.get_count()
                    print(f"joystick {event.device_index} connected\n"
                          f"\tactual joysticks: {joy_count}")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    joy_count = pygame.joystick.get_count()
                    print(f"joystick {event.instance_id} disconnected\n"
                          f"\tactual joysticks: {joy_count}")

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
