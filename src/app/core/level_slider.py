from typing import Dict, Optional, Type
import logging
from app.levels.level import Level
from app.levels.level_1 import Level1
from app.levels.level_2 import Level2
from app.levels.level_3 import Level3
from app.levels.level_4 import Level4
from app.levels.level_5 import Level5
from app.levels.level_6 import Level6
from app.levels.level_7 import Level7
from app.levels.level_8 import Level8
from app.levels.level_9 import Level9
from app.levels.level_10 import Level10
from app.pplay.window import Window
from app.entities.potato import Potato


class LevelSlider:
    def __init__(self, window: Window, start_level: int = 1):
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.level_classes: Dict[int, Type[Level]] = {
            1: Level1,
            2: Level2,
            3: Level3,
            4: Level4,
            5: Level5,
            6: Level6,
            7: Level7,
            8: Level8,
            9: Level9,
            10: Level10,
        }
        self.max_level = max(list(self.level_classes.keys()))
        self.min_level = min(list(self.level_classes.keys()))
        self.current_level_number = start_level
        self.levels: Dict[int, Optional[Level]] = {}
        self.potato = Potato(int(window.width // 2), int(window.height // 2))
        self._load_level_window()

    def _get_safe_level(self, level_number: int) -> Optional[Level]:
        """Helper method to safely get a level from the levels dictionary."""
        return self.levels.get(level_number)

    def _save_potato_state(self) -> None:
        """Save current potato state from the current level."""
        current = self._get_safe_level(self.current_level_number)
        if current is not None:
            self.potato = current.get_potato()

    def _position_potato(self, x_position: float, moving_up: bool) -> None:
        """Position the potato based on the direction of movement."""
        self.potato.x = x_position
        if moving_up:
            self.potato.y = self.window.height - 150
        else:
            self.potato.y = 50
        # Update rect to match position
        self.potato.rect.x = self.potato.x  # type: ignore
        self.potato.rect.y = self.potato.y

    def _load_level_window(self) -> None:
        """Load levels around the current level number."""
        # Save potato state if current level exists
        if (
            self.current_level_number in self.levels
            and self.levels[self.current_level_number]
        ):
            self._save_potato_state()

        # Clear existing levels
        self.levels.clear()

        # Load levels in window around current level
        for offset in [-2, -1, 0, 1, 2]:
            level_num = self.current_level_number + offset
            if self.min_level <= level_num <= self.max_level:
                level_class = self.level_classes.get(level_num)
                if level_class:
                    level = level_class(self.window, level_num, self.potato)
                    # Register level change observer
                    level.set_level_change_observer(self._handle_level_transition)
                    self.levels[level_num] = level
                    self.logger.info(f"Loaded level {level_num}")
            else:
                self.levels[level_num] = None

    def _handle_level_transition(self, new_level: int) -> None:
        """Handle transition to a new level."""
        if self.min_level <= new_level <= self.max_level:
            self.logger.info(f"Level transition triggered to level {new_level}")
            # Save potato state
            self._save_potato_state()
            x_position = self.potato.x

            # Whether we're moving up in levels
            moving_up = new_level > self.current_level_number

            # Update level
            self.current_level_number = new_level
            self._load_level_window()

            # Position potato based on direction
            self._position_potato(x_position, moving_up)

    @property
    def current_level(self) -> Level:
        """Get the current level, raising an error if it's not loaded."""
        level = self._get_safe_level(self.current_level_number)
        if level is None:
            raise ValueError(f"Level {self.current_level_number} not loaded")
        return level

    def go_to_level(self, level_number: int) -> bool:
        """Navigate to a specific level number."""
        if self.min_level <= level_number <= self.max_level:
            self._save_potato_state()
            self.current_level_number = level_number
            self._load_level_window()
            self.logger.info(f"Switched to level {self.current_level_number}")
            return True
        return False

    def update(self, delta_time: float) -> None:
        """Update the current level."""
        current = self._get_safe_level(self.current_level_number)
        if current is not None:
            current.update(delta_time)
            # We no longer need to check for level changes here,
            # as the level will notify us via the observer pattern

    def draw(self, window: Window) -> None:
        """Draw the current level."""
        current = self._get_safe_level(self.current_level_number)
        if current is not None:
            current.draw(window)
