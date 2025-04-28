import logging
from app.pplay.sprite import Sprite
from app.pplay.window import Window
from app.seedwork.path_helper import asset_path


class Game:
    def __init__(self, window: Window):
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.running = True
        self.logger.info("Game initialized")

        self.ball = Sprite(asset_path("images", "ball.png"))
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2

    def update(self, delta_time: float) -> None:
        self.window.update()

    def draw(self) -> None:
        self.window.set_background_color((0, 0, 0))
        self.ball.draw()

    def run(self) -> None:
        self.logger.info("Starting game loop")
        while self.running:
            self.update(self.window.delta_time())
            self.draw()
            self.window.update()
