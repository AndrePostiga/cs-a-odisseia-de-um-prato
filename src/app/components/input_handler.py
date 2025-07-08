from app.pplay.keyboard import Keyboard
from typing import Tuple


class InputHandler:
    def __init__(self):
        self.keyboard = Keyboard()

    def get_movement_input(self) -> Tuple[bool, bool, bool]:
        left = self.keyboard.key_pressed("LEFT")
        right = self.keyboard.key_pressed("RIGHT")
        jump = self.keyboard.key_pressed("SPACE")
        return left, right, jump

    def get_debug_movement_input(self) -> Tuple[bool, bool, bool, bool]:
        left = self.keyboard.key_pressed("LEFT")
        right = self.keyboard.key_pressed("RIGHT")
        up = self.keyboard.key_pressed("UP")
        down = self.keyboard.key_pressed("DOWN")
        return left, right, up, down

    def get_toggle_debug_input(self) -> bool:
        return self.keyboard.key_pressed("F1")
