from app.core.game_object import AbstractGameObject
from app.pplay.window import Window
from pygame.surface import Surface
from pygame.sprite import Sprite


class Tile(AbstractGameObject, Sprite):
    def __init__(self, x: int, y: int, surf: Surface):
        Sprite.__init__(self)
        AbstractGameObject.__init__(self)
        self.x = x
        self.y = y
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.image = surf
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, delta_time: float) -> None:
        pass

    def on_collision(self, other: "AbstractGameObject") -> None:
        pass

    def draw(self, window: Window) -> None:
        if window.screen is None:
            raise NotImplementedError("Window is None or not initialized")

        window.screen.blit(self.image, self.rect)
