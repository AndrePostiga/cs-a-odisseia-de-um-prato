from app.pplay.window import Window
from app.components.transform import Transform
from app.components.render import Render
from pygame.surface import Surface
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, x: int, y: int, surf: Surface):
        Sprite.__init__(self)

        # Initialize components
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.transform = Transform(x, y, self.width, self.height)
        self.render_component = Render()

        # Store the surface for rendering
        self.image = surf
        self.rect = self.transform.rect

    def update(self, delta_time: float) -> None:
        self.render_component.update(delta_time)
        self.rect = self.transform.rect

    def draw(self, window: Window) -> None:
        if window.screen is None:
            raise NotImplementedError("Window is None or not initialized")

        print("Drawing tile at position:", self.transform.x, self.transform.y)
        self.render_component.draw(window, self.transform)

    # Properties for backward compatibility
    @property
    def x(self) -> float:
        return self.transform.x

    @property
    def y(self) -> float:
        return self.transform.y
