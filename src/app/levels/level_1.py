from app.entities.potato import Potato
from app.levels.level import Level
from app.pplay.window import Window


class Level1(Level):
    def __init__(
        self, window: Window, level_number: int, main_character: Potato
    ) -> None:
        super().__init__(window, level_number, main_character)

    def load_map(self) -> None:
        self.tilemap.load_map(f"map_{self.level_number}")

    def draw(self, window: Window) -> None:
        self.tilemap.draw(self.window)
        self.main_character.draw(window)
