from typing import Tuple
import pygame
from pygame.sprite import Group, Sprite


class Tile(Sprite):
    def __init__(
        self, pos: Tuple[int, int], surf: pygame.Surface, group: Group
    ) -> None:
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
