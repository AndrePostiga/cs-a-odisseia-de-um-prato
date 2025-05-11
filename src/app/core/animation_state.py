from enum import Enum, auto


class AnimationState(Enum):
    IDLE = auto()
    JUMP = auto()
    FALL = auto()
    RUN = auto()
    CLIMB = auto()
