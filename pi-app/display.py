from pathlib import Path

import pygame
from pygame.surface import Surface

ANIM_DIR = Path(__file__).parent / "animations"
STATES = ["idle", "listening", "talking", "boot", "thinking", "error"]
FPS = 30
FRAME_MS = 1000 // 12  # animations at 12 fps
BOOT_FALLBACK_MS = 3000

# placeholder colours when no animation frames
PLACEHOLDER: dict[str, tuple[int, int, int]] = {
    "idle": (120, 10, 20),
    "listening": (0, 230, 255),
    "talking": (255, 40, 60),
    "boot": (240, 250, 255),
    "thinking": (255, 255, 255),
    "error": (100, 110, 50),
}


class Display:
    def __init__(self, fullscreen: bool = False, flip_x: bool = False, flip_y: bool = False):
        _ = pygame.init()
        if fullscreen:
            # screen size 720 x 1280
            self.screen: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((360, 640))
        pygame.display.set_caption("n3-D3ck")
        _ = pygame.mouse.set_visible(False)

        self.size: tuple[int, int] = self.screen.get_size()
        self.flip_x: bool = flip_x
        self.flip_y: bool = flip_y
        self.frames: dict[str, list[Surface]] = {state: self._load(state) for state in STATES}

        self.state: str = "idle"
        self.index: int = 0
        self.last_step: int = 0
        self.boot_started: int = 0

    def _load(self, state: str) -> list[Surface]:
        """Load animations/<state>/*.png in name order, scaled to the screen."""
        folder = ANIM_DIR / state
        if not folder.is_dir():
            return []
        frames: list[Surface] = []
        for path in sorted(folder.glob("*.png")):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.smoothscale(image, self.size)
            if self.flip_x or self.flip_y:
                image = pygame.transform.flip(image, self.flip_x, self.flip_y)
            frames.append(image)
        return frames

    def set_state(self, state: str) -> None:
        if state not in STATES:
            raise ValueError(f"unknown state: {state!r}")
        if state != self.state:
            self.state = state
            self.index = 0
            self.last_step = pygame.time.get_ticks()
        if state == "boot":
            self.boot_started = pygame.time.get_ticks()

    def get_state(self) -> str:
        return self.state

    def update(self, now: int) -> None:
        frames = self.frames[self.state]

        if frames and now - self.last_step >= FRAME_MS:
            self.last_step = now
            self.index += 1
            if self.index >= len(frames):
                if self.state == "boot":
                    # boot plays once, then falls back to idle
                    self.set_state("idle")
                if (
                    self.state == "boot"
                    and not self.frames["boot"]
                    and now - self.boot_started >= BOOT_FALLBACK_MS
                ):
                    self.set_state("idle")
                    frames = self.frames[self.state]
                self.index = 0

        if frames:
            _ = self.screen.blit(frames[self.index], (0, 0))
        else:
            _ = self.screen.fill(PLACEHOLDER[self.state])

        pygame.display.flip()
