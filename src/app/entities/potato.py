from typing import Optional, Callable
from app.core.game_object import AbstractGameObject
from app.pplay.window import Window
from app.core.animator import Animator, AnimationData
from app.core.animation_state import AnimationState
from app.seedwork.path_helper import asset_path
from app.core.physics import WallSide
import pygame
from app.pplay.keyboard import Keyboard


class Potato(AbstractGameObject):
    def __init__(self, x: int, y: int):
        AbstractGameObject.__init__(self)
        self.state = AnimationState.IDLE
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.animator = self.create_animator()
        self.timer = 0.0
        self.keyboard = Keyboard()
        self.speed = 1000
        # Wall collision handler callback
        self.wall_collision_handler: Optional[Callable[[WallSide], None]] = None

    def create_animator(self) -> Animator:
        idle = [
            pygame.transform.scale(
                pygame.image.load(
                    asset_path("images", "characters", "elf", "idle", f"{i}.png")
                ).convert_alpha(),
                (50 * 3, 50 * 3),
            )
            for i in range(4)
        ]
        run = [
            pygame.transform.scale(
                pygame.image.load(
                    asset_path("images", "characters", "elf", "run", f"{i}.png")
                ).convert_alpha(),
                (50 * 3, 50 * 3),
            )
            for i in range(2)
        ]

        return Animator(
            {
                AnimationState.IDLE: AnimationData(frames=idle, frame_duration=0.1),
                AnimationState.RUN: AnimationData(frames=run, frame_duration=0.2),
            }
        )

    def _change_state(self, state: AnimationState) -> None:
        if state != self.state:
            self.state = state
            self.animator.set_state(state)

    def handle_movement(self, delta_time: float) -> None:
        moved = False

        if self.keyboard.key_pressed("left"):
            self.x -= int(self.speed * delta_time)
            moved = True
        if self.keyboard.key_pressed("right"):
            self.x += int(self.speed * delta_time)
            moved = True

        if self.keyboard.key_pressed("up"):
            self.y -= int(self.speed * delta_time)
            moved = True
        if self.keyboard.key_pressed("down"):
            self.y += int(self.speed * delta_time)
            moved = True

        if moved:
            self._change_state(AnimationState.RUN)
        else:
            self._change_state(AnimationState.IDLE)

    def set_wall_collision_handler(self, handler: Callable[[WallSide], None]) -> None:
        """Set a handler to be called when this potato collides with a wall"""
        self.wall_collision_handler = handler

    def on_wall_collision(self, wall_side: WallSide) -> None:
        # Handle basic blocking collision with side walls
        if wall_side == WallSide.LEFT:
            self.x = 5
        elif wall_side == WallSide.RIGHT:
            self.x = self.rect.x - 5

        # Call the external handler for level transition logic
        if self.wall_collision_handler and (
            wall_side == WallSide.TOP or wall_side == WallSide.BOTTOM
        ):
            self.wall_collision_handler(wall_side)

    def on_collision(self, other: AbstractGameObject) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.handle_movement(delta_time)
        self.animator.update(delta_time)
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, window: Window) -> None:
        if window.screen is None:
            raise ValueError("Window screen is None")
        window.screen.blit(self.animator.get_current_frame(), (self.x, self.y))
