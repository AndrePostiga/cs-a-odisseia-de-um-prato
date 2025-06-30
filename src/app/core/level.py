from app.entities.potato import Potato
from app.pplay.window import Window
from typing import List, Tuple, Optional, Any
from app.seedwork.tilemap_loader import load_tilemap_groups  # type: ignore
from app.entities.tile import Tile
from app.core.tilemap_group import TilemapGroup
import logging
import random
import pygame


class Level:
    def __init__(self, window: Window, level_number: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.level_number = level_number

        self.main_character: Optional[Potato] = None

        # Map
        self.tiles: List[Tile] = []
        self.tilemap_layers: List[Tuple[TilemapGroup, Any]] = []
        self.random_background_color: Optional[Tuple[int, int, int]] = None
        self._load_map()

    def _load_map(self) -> None:
        try:
            self.tilemap_layers = load_tilemap_groups(f"map_{self.level_number}")
            self.tiles = []

            # Tiles que de fato eu preciso detectar colisão
            for group_type, group in self.tilemap_layers:
                if group_type == TilemapGroup.INTERACTIVE_BLOCK:
                    for tile in group:
                        self.tiles.append(tile)

        except Exception as e:
            self.logger.error(f"Error loading map: {e}")
            self.random_background_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

    def set_main_character(self, main_character: Potato) -> None:
        self.logger.info(f"Setting main character: {main_character}")
        self.main_character = main_character

    def update(self, delta_time: float) -> None:
        if self.main_character:
            self.main_character.update(delta_time)
            self.main_character.safe_move(
                delta_time=delta_time,
                tiles=self.tiles,
                window_width=self.window.width,
                window_height=self.window.height,
            )

    def draw(self) -> None:
        # Desenha fundo colorido caso não tenha carregado mapa (levels incompletos)
        if self.random_background_color:
            self.window.set_background_color(self.random_background_color)
        else:
            self._draw_tilemap_layers()

        if self.main_character:
            self.main_character.draw(self.window)

    def _draw_tilemap_layers(self) -> None:
        # 1. desenha background primeiro
        for group_type, group in self.tilemap_layers:
            if group_type == TilemapGroup.BACKGROUND:
                for background_tile in group:
                    background_tile.draw(self.window)

        # 2. desenha blocos interativos
        for group_type, group in self.tilemap_layers:
            if group_type == TilemapGroup.INTERACTIVE_BLOCK:
                group.draw(self.window.screen)
                # self._debug_draw(self.window, group)

        # 3. desenha cenário pode ter blocos sobrepostos desenhados depois
        for group_type, group in self.tilemap_layers:
            if group_type in [TilemapGroup.SCENERY_BLOCK, TilemapGroup.SCENERY_OBJECT]:
                group.draw(self.window.screen)
                # self._debug_draw(self.window, group)

    def _debug_draw(self, window: Window, tilegroup: List[Tile]) -> None:
        if window.screen is None:
            raise NotImplementedError("Window is None or not initialized")

        for tile in tilegroup:
            pygame.draw.rect(window.screen, (255, 0, 0), tile.rect, 2)
