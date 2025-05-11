from app.entities.potato import Potato
from app.levels.level import Level
from app.pplay.window import Window


class Level2(Level):
    def __init__(
        self, window: Window, level_number: int, main_character: Potato
    ) -> None:
        super().__init__(window, level_number, main_character)

    def load_map(self) -> None:
        # No tilemap loading for level 2
        pass

    def draw(self, window: Window) -> None:
        window.set_background_color((0, 255, 0))  # Green
        self.main_character.draw(window)
