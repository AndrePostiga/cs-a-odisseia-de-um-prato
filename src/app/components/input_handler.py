from app.pplay.keyboard import Keyboard
from typing import Tuple


class InputHandler:
    def __init__(self):
        self.keyboard = Keyboard()

    def get_movement_input(self) -> Tuple[bool, bool, bool]:
        return (
            self.keyboard.key_pressed("left")
            or self.keyboard.key_pressed("a")
            or self.keyboard.key_pressed("A"),
            self.keyboard.key_pressed("right")
            or self.keyboard.key_pressed("d")
            or self.keyboard.key_pressed("D"),
            self.keyboard.key_pressed("space"),
        )
