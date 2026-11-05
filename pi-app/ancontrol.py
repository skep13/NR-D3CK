#animation control

import time
from typing import ClassVar

from display import Display


class AnimationControl:

    VALID_STATES: ClassVar[set[str]] = {
        "idle",
        "listening",
        "talking",
        "boot",
        "thinking",
        "error",
    }

    def __init__(self, display: Display) -> None:

        self.display: Display = display
        self.current_state: str = "boot"

        self.boot_complete: bool = False
        self.last_activity: float = time.monotonic()

        self.idle_timeout: float = 10

        self.display.set_state("boot")

        print("[NR animation] controller on")

    def set_state(self, state: str) -> bool:

        if state not in self.VALID_STATES:
            print(f"[NR animation] invalid: {state}")
            return False

        try:
            self.display.set_state(state)
            self.current_state = state
            self.last_activity = time.monotonic()

            print(f"[NR animation] {state.upper()}")

            return True

        except ValueError as error:
            print(f"[NR animation] display error: {error}")
            return False

    def idle(self) -> bool:
        return self.set_state("idle")

    def listen(self) -> bool:
        return self.set_state("listening")

    def think(self) -> bool:
        return self.set_state("thinking")

    def talk(self) -> bool:
        return self.set_state("talking")

    def error(self) -> bool:
        return self.set_state("error")

    def boot(self) -> bool:
        return self.set_state("boot")

    def update(self) -> None:

        #detects display once its booted
        if (
            self.current_state == "boot"
            and self.display.get_state() == "idle"
        ):
            self.boot_complete = True
            self.current_state = "idle"

            print("[NR animation] boot successful")

        #return to idle after inactivity
        if self.current_state in {
            "listening",
            "thinking",
            "talking",
        }:
            elapsed = time.monotonic() - self.last_activity
            if elapsed >= self.idle_timeout:
                _ = self.idle()

    def get_current_state(self) -> str:
        return self.current_state
