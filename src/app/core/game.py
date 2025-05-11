import logging
from app.pplay.window import Window
from app.core.level_slider import LevelSlider


class Game:
    def __init__(self, window: Window):
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.running = True
        self.logger.info("Game initialized")
        self.window.set_background_color((0, 0, 0))
        self.level_slider = LevelSlider(window)

    def run(self) -> None:
        self.logger.info("Starting game loop")
        while self.running:
            delta_time = self.window.delta_time()
            self.window.set_background_color((0, 0, 0))
            self.level_slider.update(delta_time)
            self.level_slider.draw(self.window)
            self.window.update()
