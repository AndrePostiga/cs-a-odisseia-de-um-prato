from enum import Enum, auto


class TilemapGroup(Enum):
    BACKGROUND = auto()
    INTERACTIVE_BLOCK = auto()
    SCENERY_BLOCK = auto()
    SCENERY_OBJECT = auto()
