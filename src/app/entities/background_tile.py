from pygame.surface import Surface
from pygame.sprite import Sprite
from app.pplay.window import Window
from app.components.transform import Transform
from app.components.render import Render
import pygame


class BackgroundTile(Sprite):
    def __init__(self, surf: Surface):
        Sprite.__init__(self)

        # Initialize components
        self.width = surf.get_width()
        self.height = surf.get_height()
        self.transform = Transform(0, 0, self.width, self.height)
        self.render_component = Render()

        # Store the surface for rendering
        self.image = surf
        self.rect = self.transform.rect

    def update(self, delta_time: float) -> None:
        # Update components
        self.render_component.update(delta_time)
        # Sync rect with transform
        self.rect = self.transform.rect

    def draw(self, window: Window) -> None:
        if window.screen is None:
            raise NotImplementedError("Window is None or not initialized")

        image_width = self.image.get_width()
        window_width: int = window.width

        # Draw tiled background across the screen width
        for x in range(0, window_width, image_width):
            window.screen.blit(self.image, (x, 0))

        # Draw red debug rectangle around background tile
        pygame.draw.rect(window.screen, (255, 0, 0), self.transform.rect, 2)
