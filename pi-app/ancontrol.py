#animation cotnrol

from pickle import FALSE
import time

class AnimationControl

VALID_STATES = {
    "idle",
    "listening",
    "talking",
    "boot",
    "thinking",
    "error",
}

def __init__(self, display):

    self.display = display
    self.current_state = "boot"

    self.boot_complete = FALSE
    self.last_activity = time.monotonic()

    self.idle_timeout = 10

    self.display.set_state("boot")

    print("[NR animation] controller on")

def set_state(self, state):

    if state not in self.VALID_STATES:
        print(f"[NR animation] invalid: {state}")
        return False
    
    try:
        self.display.set_state(state)
        self.current_state = state
        self.last_activity = time.monotonic()

        print(f"[NR animation]") {state.upper()}") 

        return True
    
    except ValueError as error:
        print(f"[NR animation] display error: {error}")
        return False


def idle(self):
    return self.set_state("idle")

def listen(self):
    return self.set_state("listening")

def think(self):
    return self.set_state("think")

def talk(self):
    return self.set_state("talking")

def error(self):
    return self.set_state("error")

def boot(self):
    return self.set_state("boot")

def update(self):

    #detects display once its booted

if( 
    self.current_state == "boot"
    and self.display.get_state() == "idle"
):
    self.boot_complete = True
    self.current_state = "idle"

    print("[NR animation] boot successful")

    #return to idle

if self.current_state in {
    "listening",
    "thinking",
    "talking",
}:
    elapsed >= self.idle_timeout:
    self.idle()

def get_current_state(self):
    return self.current_state