from abc import ABC, abstractmethod
from typing import Any
from app.pplay.window import Window


class AbstractGameObject(ABC):
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def collided(self, other: "AbstractGameObject") -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )

    def on_collision(self, other: "AbstractGameObject") -> None:
        pass

    def on_wall_collision(self, wall_side: Any) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    @abstractmethod
    def draw(self, window: Window) -> None:
        pass
