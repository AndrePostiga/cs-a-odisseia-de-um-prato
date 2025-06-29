import pygame
from app.core.animator import Animator, AnimationData
from app.core.animation_state import AnimationState
from app.seedwork.path_helper import asset_path


class AnimationComponent:
    def __init__(self, scale: float = 1.5):
        self.scale = scale
        self.state = AnimationState.IDLE
        self.facing_right = True
        self.animator = self._create_animator()

    def _load_image_and_scale(self, scale: float, *path_parts: str) -> pygame.Surface:
        image_path = asset_path(*path_parts)
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(
            image, (image.get_width() * scale, image.get_height() * scale)
        )
        return scaled_image

    def _create_animator(self) -> Animator:
        idle = [
            self._load_image_and_scale(
                self.scale, "images", "characters", "potato", "idle", f"{i}.png"
            )
            for i in range(1, 6)
        ]
        run = [
            self._load_image_and_scale(
                self.scale, "images", "characters", "potato", "run", f"{i}.png"
            )
            for i in range(1, 5)
        ]
        jump = [
            self._load_image_and_scale(
                self.scale, "images", "characters", "potato", "jump", "1.png"
            )
        ]

        return Animator(
            {
                AnimationState.IDLE: AnimationData(frames=idle, frame_duration=0.1),
                AnimationState.RUN: AnimationData(frames=run, frame_duration=0.2),
                AnimationState.JUMP: AnimationData(frames=jump, frame_duration=0.3),
            }
        )

    def change_state(self, new_state: AnimationState) -> None:
        if new_state != self.state:
            self.state = new_state
            self.animator.set_state(new_state)

    def set_facing_direction(self, facing_right: bool) -> None:
        self.facing_right = facing_right

    def get_current_frame(self) -> pygame.Surface:
        frame = self.animator.get_current_frame()

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def get_frame_dimensions(self) -> tuple[int, int]:
        frame = self.get_current_frame()
        return frame.get_width(), frame.get_height()

    def update(self, delta_time: float) -> None:
        self.animator.update(delta_time)
