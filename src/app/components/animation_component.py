import pygame
from app.core.animator import Animator, AnimationData
from app.core.animation_state import AnimationState
from app.seedwork.path_helper import asset_path


class AnimationComponent:
    def __init__(self, character_name: str, scale: float = 1.5):
        self.character_name = character_name
        self.scale = scale
        self.state = AnimationState.IDLE
        self.facing_right = True
        self.animator = self._create_animator()

    def _load_image_and_scale(self, scale: float, *path_parts: str) -> pygame.Surface:
        image_path = asset_path(*path_parts)
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(
            image,
            (int(image.get_width() * scale), int(image.get_height() * scale)),
        )
        return scaled_image

    def _create_animator(self) -> Animator:
        animations = {}

        # Mapeia estados de animação para pastas e contagens de frames
        animation_map = {
            "potato": {
                AnimationState.IDLE: ("idle", 6),
                AnimationState.RUN: ("run", 5),
                AnimationState.JUMP: ("jump", 1),
            },
            "butter": {AnimationState.IDLE: ("idle", 5)},
            "cheese": {AnimationState.IDLE: ("idle", 5)},
            "dried_meat": {AnimationState.IDLE: ("idle", 5)},
            "milk": {AnimationState.IDLE: ("idle", 5)},
        }

        char_animations = animation_map.get(self.character_name, {})

        for state, (folder, frame_count) in char_animations.items():
            path_parts = ["images", "characters", self.character_name, folder]

            frames = [
                self._load_image_and_scale(self.scale, *path_parts, f"{i}.png")
                for i in range(1, frame_count + 1)
            ]

            frame_duration = 0.1 if state == AnimationState.IDLE else 0.2
            animations[state] = AnimationData(
                frames=frames, frame_duration=frame_duration
            )

        return Animator(animations)

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
