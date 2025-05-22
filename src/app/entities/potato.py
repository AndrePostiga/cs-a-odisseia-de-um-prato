from app.core.game_object import AbstractGameObject
from app.core.observer import Observable
from app.entities.tile import Tile
from app.pplay.window import Window
from app.core.animator import Animator, AnimationData
from app.core.animation_state import AnimationState
from app.seedwork.path_helper import asset_path
from app.core.physics import WallSide
from app.pplay.keyboard import Keyboard
import pygame
import logging


class Potato(AbstractGameObject, Observable):
    def __init__(self, x: int, y: int):
        self.logger = logging.getLogger(__name__)
        AbstractGameObject.__init__(self)
        Observable.__init__(self)
        self.state = AnimationState.IDLE
        self.x = x
        self.y = y

        self.animator = self.create_animator()

        first_frame = self.animator.get_current_frame()
        self.width = first_frame.get_width()
        self.height = first_frame.get_height()
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.timer = 0.0
        self.keyboard = Keyboard()
        self.speed = 1000
        self.vx = 0
        self.vy = 0

        self.gravity = 10
        self.jump_strength = -3000
        self.is_on_ground = False

    def _load_image_and_scale(self, scale: int, *path_parts: str) -> pygame.Surface:
        image_path = asset_path(*path_parts)
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(
            image, (image.get_width() * scale, image.get_height() * scale)
        )
        return scaled_image

    def create_animator(self) -> Animator:
        scale = 4
        idle = [
            self._load_image_and_scale(
                scale, "images", "characters", "elf", "idle", f"{i}.png"
            )
            for i in range(4)
        ]
        run = [
            self._load_image_and_scale(
                scale, "images", "characters", "elf", "run", f"{i}.png"
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
        # Reset horizontal velocity only
        self.vx = 0
        moved = False

        # Horizontal movement
        if self.keyboard.key_pressed("left"):
            self.vx = -self.speed
            moved = True
        if self.keyboard.key_pressed("right"):
            self.vx = self.speed
            moved = True

        # Jump only when space is pressed AND on ground
        if self.keyboard.key_pressed("space") and self.is_on_ground:
            self.vy = self.jump_strength
            self.is_on_ground = False

        # ALWAYS apply gravity (this creates smooth acceleration)
        self.vy += int(self.gravity)

        # Update animation state (outside the gravity condition)
        if moved:
            self._change_state(AnimationState.RUN)
        else:
            self._change_state(AnimationState.IDLE)

    def on_wall_collision(self, wall_side: WallSide) -> None:
        if wall_side == WallSide.LEFT:
            self.x = 5
        elif wall_side == WallSide.RIGHT:
            self.x = self.rect.x - 5

        if wall_side == WallSide.TOP:
            self.logger.info("Hit top wall")
            self.notify_observers("hit_top_wall")
        elif wall_side == WallSide.BOTTOM:
            self.logger.info("Hit bottom wall")
            self.notify_observers("hit_bottom_wall")

    def on_collision(self, other: AbstractGameObject) -> None:
        if isinstance(other, Tile):
            # Colliding with top of a tile (landing)
            if (
                self.vy > 0
                and self.rect.bottom >= other.rect.top
                and self.rect.top < other.rect.top
            ):
                self.y = other.rect.top - self.height
                self.vy = 0
                self.is_on_ground = True  # Character is on ground now

            # Hitting ceiling
            elif (
                self.vy < 0
                and self.rect.top <= other.rect.bottom
                and self.rect.bottom > other.rect.bottom
            ):
                self.y = other.rect.bottom
                self.vy = 0

            # Horizontal collisions remain similar
            elif (
                self.vx > 0
                and self.rect.right >= other.rect.left
                and self.rect.left < other.rect.left
            ):
                self.x = other.rect.left - self.width
                self.vx = 0
            elif (
                self.vx < 0
                and self.rect.left <= other.rect.right
                and self.rect.right > other.rect.right
            ):
                self.x = other.rect.right
                self.vx = 0

    def update(self, delta_time: float) -> None:
        self.handle_movement(delta_time)

        self.is_on_ground = False

        self.x += int(self.vx * delta_time)
        self.y += int(self.vy * delta_time)
        self.animator.update(delta_time)
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, window: Window) -> None:
        if window.screen is None:
            raise ValueError("Window screen is None")
        pygame.draw.rect(window.screen, (255, 0, 0), self.rect, 1)
        window.screen.blit(self.animator.get_current_frame(), (self.x, self.y))
