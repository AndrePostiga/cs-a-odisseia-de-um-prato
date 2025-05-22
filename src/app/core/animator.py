import pygame
from typing import Dict, List
from app.core.animation_state import AnimationState
from dataclasses import dataclass


@dataclass
class AnimationData:
    frames: List[pygame.Surface]
    frame_duration: float


class Animator:
    def __init__(
        self,
        animations: Dict[AnimationState, AnimationData],
        default_frame_duration: float = 0.2,
    ):
        self._animations = animations
        self._default_frame_duration = default_frame_duration
        self._state = AnimationState.IDLE
        self._frame_index = 0
        self._elapsed = 0.0

    def set_state(self, state: AnimationState) -> None:
        if state != self._state:
            self._state = state
            self._frame_index = 0
            self._elapsed = 0

    def update(self, dt: float) -> None:
        animation_data = self._animations[self._state]
        self._elapsed += dt

        frame_duration = animation_data.frame_duration
        if self._elapsed >= frame_duration:
            self._elapsed %= frame_duration
            self._frame_index = (self._frame_index + 1) % len(animation_data.frames)

    def get_current_frame(self) -> pygame.Surface:
        return self._animations[self._state].frames[self._frame_index]
