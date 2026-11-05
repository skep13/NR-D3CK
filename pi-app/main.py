import argparse
import pygame
from display import Display, FPS

KEYS = {
    pygame.K_1: "idle",
    pygame.K_2: "listening",
    pygame.K_3: "talking",
    pygame.K_4: "boot",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullscreen", action="store_true")
    args = parser.parse_args()

    display = Display(fullscreen=args.fullscreen)
    display.set_state("boot")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in KEYS:
                    display.set_state(KEYS[event.key])

        display.update(pygame.time.get_ticks())
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
