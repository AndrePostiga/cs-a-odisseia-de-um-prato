import pygame
from typing import Optional
from app.pplay.window import Window
from app.components.animation_component import AnimationComponent
from app.components.transform import Transform


class Render:
    """Handles drawing the entity."""

    def __init__(self, animation_component: Optional["AnimationComponent"] = None):
        self.animation_component = animation_component
        self.debug_draw = False  # Can be toggled

    def draw(self, window: Window, transform: Transform):
        if window.screen is None:
            raise ValueError("Window screen is None")

        if self.debug_draw:
            pygame.draw.rect(window.screen, (255, 0, 0), transform.rect, 2)

        if self.animation_component:
            current_frame = self.animation_component.get_current_frame()
            window.screen.blit(current_frame, (int(transform.x), int(transform.y)))

    def update(self, delta_time: float):
        """Update animations."""
        if self.animation_component:
            self.animation_component.update(delta_time)
