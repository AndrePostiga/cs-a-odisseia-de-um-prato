import logging
from typing import List
from enum import Enum, auto
from app.pplay.window import Window
from app.core.game_object import AbstractGameObject
from app.entities.tile import Tile


class WallSide(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


class Physics:
    def __init__(
        self, window: Window, game_objects: List[AbstractGameObject], tiles: List[Tile]
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.screen_width = window.width
        self.screen_height = window.height
        self.top_boundary = 0
        self.bottom_boundary = self.screen_height
        self.left_boundary = 0
        self.right_boundary = self.screen_width
        self.game_objects: List[AbstractGameObject] = game_objects
        self.tiles: List[Tile] = tiles

    def _check_wall_collision(self, obj: AbstractGameObject) -> None:
        if obj.x < self.left_boundary:
            obj.on_wall_collision(WallSide.LEFT)

        elif obj.x + obj.width > self.right_boundary:
            obj.on_wall_collision(WallSide.RIGHT)

        if obj.y < self.top_boundary:
            obj.on_wall_collision(WallSide.TOP)

        elif obj.y + obj.height > self.bottom_boundary:
            obj.on_wall_collision(WallSide.BOTTOM)

    def _check_object_collisions(self) -> None:
        for i in range(len(self.game_objects)):
            for j in range(i + 1, len(self.game_objects)):
                obj1 = self.game_objects[i]
                obj2 = self.game_objects[j]

                if obj1.collided(obj2):
                    obj1.on_collision(obj2)
                    obj2.on_collision(obj1)

    def _check_tile_collisions(self) -> None:
        if not self.tiles:
            return

        for obj in self.game_objects:
            # Define uma área de busca ao redor do objeto
            search_range = 100

            # Calcula a região ao redor do objeto para verificar
            min_x = obj.x - search_range
            max_x = obj.x + obj.width + search_range
            min_y = obj.y - search_range
            max_y = obj.y + obj.height + search_range

            # Verifica apenas tiles dentro desta área
            for tile in self.tiles:
                if (
                    tile.x < max_x
                    and tile.x + tile.width > min_x
                    and tile.y < max_y
                    and tile.y + tile.height > min_y
                ):
                    if obj.collided(tile):
                        obj.on_collision(tile)
                        tile.on_collision(obj)

    def update(self, delta_time: float) -> None:
        for obj in self.game_objects:
            self._check_wall_collision(obj)

        self._check_object_collisions()
        self._check_tile_collisions()
