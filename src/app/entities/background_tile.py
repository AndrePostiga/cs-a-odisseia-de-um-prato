from pygame.surface import Surface
from app.pplay.window import Window
from app.entities.tile import Tile


class BackgroundTile(Tile):
    def __init__(self, surf: Surface):
        super().__init__(0, 0, surf)

    def draw(self, window: Window) -> None:
        image_width = self.image.get_width()

        window_width: int = window.width
        for x in range(0, window_width, image_width):
            window.screen.blit(self.image, (x, 0))  # type: ignore
