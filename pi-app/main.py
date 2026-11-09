import argparse
from typing import cast

import pygame
from display import Display, FPS
from ancontrol import AnimationControl

KEYS = {
    pygame.K_1: "idle",
    pygame.K_2: "listening",
    pygame.K_3: "talking",
    pygame.K_4: "boot",
    pygame.K_5: "thinking",
    pygame.K_6: "error",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--fullscreen", action="store_true")
    args = parser.parse_args()
    fullscreen = cast(bool, args.fullscreen)

    display = Display(fullscreen=fullscreen)
    animation = AnimationControl(display)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = cast(int, event.key)
                if key == pygame.K_ESCAPE:
                    running = False
                elif key in KEYS:
                    _ = animation.set_state(KEYS[key])

        display.update(pygame.time.get_ticks())
        animation.update()
        _ = clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
