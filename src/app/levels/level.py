from abc import abstractmethod
from typing import List, Optional, Callable
from app.core.game_object import AbstractGameObject
from app.core.tilemap import TileMap
from app.pplay.window import Window
from app.entities.potato import Potato
from app.core.physics import Physics, WallSide


class Level(AbstractGameObject):
    def __init__(
        self, window: Window, level_number: int, main_character: Potato
    ) -> None:
        super().__init__()
        self.level_number = level_number
        self.window = window
        self.tilemap = TileMap()
        self.main_character = main_character
        self.physics = Physics(window)
        self.game_objects: List[AbstractGameObject] = []
        self.load_map()

        # Observer pattern: callback for level change notifications
        self.level_change_observer: Optional[Callable[[int], None]] = None

        # Add the main character to this level's physics system
        self.game_objects.append(self.main_character)
        self.physics.add_game_object(self.main_character)

        # Register to handle the main character's wall collisions
        self.main_character.set_wall_collision_handler(
            self.handle_character_wall_collision
        )

    def on_wall_collision(self, wall_side: WallSide) -> None:
        # This method is not used directly anymore, as the main character
        # will be the one colliding with walls, not the level itself
        pass

    def handle_character_wall_collision(self, wall_side: WallSide) -> None:
        """Handle wall collision for the main character"""
        new_level = self.level_number
        if wall_side == WallSide.TOP:
            new_level += 1
        elif wall_side == WallSide.BOTTOM:
            new_level -= 1

        # Notify observer about level change
        if self.level_change_observer and new_level != self.level_number:
            self.level_change_observer(new_level)

    def set_level_change_observer(self, observer: Callable[[int], None]) -> None:
        """Set the observer function that will be called when a level change is needed"""
        self.level_change_observer = observer

    def get_potato(self) -> Potato:
        """Return the main character (potato) for this level"""
        return self.main_character

    @abstractmethod
    def load_map(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        for obj in self.game_objects:
            obj.update(delta_time)
        self.physics.update(delta_time)
