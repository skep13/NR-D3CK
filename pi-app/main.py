import argparse
import pygame
import queue
import threading
from display import Display, FPS
from ancontrol import AnimationControl
from brain import Brain

KEYS = {
    pygame.K_1: "idle",
    pygame.K_2: "listening",
    pygame.K_3: "talking",
    pygame.K_4: "boot",
    pygame.K_5: "thinking",
    pygame.K_6: "error",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullscreen", action="store_true")
    args = parser.parse_args()

    display = Display(fullscreen=args.fullscreen)
    animation = AnimationControl(display)
    brain = Brain()
    clock = pygame.time.Clock()
    typed = queue.Queue()
    threading.Thread(target=read_terminal args=(typed,) daemon=True).start()
    print("type message press enter")

    woke_up = False
    talk_until = 0

    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in KEYS:
                    animation.set_state(KEYS[event.key])
            if animation.boot_complete and not woke_up:
                woke_up = True
                if brain.ask_async("[wake up]"):
                    animation.think()

            try:
                text = typed.get_nowait()
            except queue.Empty:
                text = None
            if text and woke_up:
                if brain.ask_async(text):
                    animation.think()
                else:
                    print("(berri still thinkinhg)")

            result = brain.get_reply()
            if result is not None:
                reply = result ["reply"]
            if reply is none:
                animation.error
            else:
                print("berri", reply)
                animation.talk()
                seconds = len(reply.split()) / WORDS_PER_SECOND
                talk_until = now + int(seconds * 1000)

        if animation.get_current_state() == "talking" and talk_until and now >= talk_until:
            talk_until = 0
            animation.idle()

        display.update(now)
        animation.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
