from app.core.game_object import AbstractGameObject
from app.entities.potato import Potato
from app.pplay.window import Window
from app.core.physics import Physics
from typing import List, Tuple
from app.seedwork.tilemap_loader import load_tilemap_groups  # type: ignore
from pygame.sprite import Group
from app.entities.tile import Tile
from app.core.tilemap_group import TilemapGroup
import logging
import random


class Level:
    def __init__(self, window: Window, level_number: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.game_objects: List[AbstractGameObject] = []
        self.level_number = level_number
        self.tilemap_layers: List[Tuple[TilemapGroup, Group[Tile]]] = []

        self.random_background_color = None
        try:
            self.tiles = self.load_map()
        except Exception as e:
            self.logger.error(f"Error loading map: {e}")
            self.random_background_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        self.physics = Physics(window, self.game_objects, self.tiles)

    def set_main_character(self, main_character: Potato) -> None:
        print("Setting main character")
        self.logger.info(f"Setting main character: {main_character}")
        self.main_character = main_character
        self.game_objects.append(main_character)

    def load_map(self) -> List[Tile]:
        tiles: List[Tile] = []
        self.logger.info(f"\n\n\nLoading map for level {self.level_number}")
        self.tilemap_layers = load_tilemap_groups(f"map_{self.level_number}")
        for group_type, group in self.tilemap_layers:
            if group_type == TilemapGroup.INTERACTIVE_BLOCK:
                for tile in group:
                    tiles.append(tile)
        return tiles

    def update(self, delta_time: float) -> None:
        for obj in self.game_objects:
            obj.update(delta_time)
        self.physics.update(delta_time)

    def draw(self) -> None:
        if self.random_background_color is None:
            # 1. Primeiro desenha o background (fundo)
            for group_type, group in self.tilemap_layers:
                if group_type == TilemapGroup.BACKGROUND:
                    for background_tile in group:
                        background_tile.draw(self.window)

            # 2. Depois desenha os blocos interativos (meio)
            for group_type, group in self.tilemap_layers:
                if group_type == TilemapGroup.INTERACTIVE_BLOCK:
                    group.draw(self.window.screen)  # type: ignore

            # 3. Por último desenha os blocos de cenário (frente)
            for group_type, group in self.tilemap_layers:
                if (
                    group_type == TilemapGroup.SCENERY_BLOCK
                    or group_type == TilemapGroup.SCENERY_OBJECT
                ):
                    group.draw(self.window.screen)  # type: ignore

        else:
            self.window.set_background_color(self.random_background_color)

        self.main_character.draw(self.window)
