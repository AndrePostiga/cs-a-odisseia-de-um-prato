from abc import ABC, abstractmethod
from typing import Any
from app.pplay.window import Window


class AbstractGameObject(ABC):
    """Abstract base class for all game objects that require update and draw methods"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def collided(self, other: "AbstractGameObject") -> bool:
        """Check if this object collides with another game object using rect collision"""
        # Use pygame's rect collision detection
        from pygame import Rect

        self_rect = Rect(self.x, self.y, self.width, self.height)
        other_rect = Rect(other.x, other.y, other.width, other.height)
        return self_rect.colliderect(other_rect)

    def on_collision(self, other: "AbstractGameObject") -> None:
        """Called when this object collides with another game object"""
        # Default implementation does nothing
        pass

    def on_wall_collision(self, wall_side: Any) -> None:
        """Called when this object collides with a wall/boundary"""
        # Default implementation does nothing
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the game object's state"""
        pass

    @abstractmethod
    def draw(self, window: Window) -> None:
        """Draw the game object"""
        pass
