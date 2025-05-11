from typing import Dict, Optional, Any
import pygame
from pytmx.util_pygame import load_pygame
from app.pplay.window import Window
from app.seedwork.path_helper import asset_path
from app.core.tile import Tile


class TileMap:
    def __init__(self) -> None:
        self.sprite_groups: Dict[str, Dict[str, pygame.sprite.Group]] = {}  # type: ignore
        self.current_map: Optional[str] = None
        self.map_data: Optional[Any] = None  # Added type hint

    def load_map(self, map_name: str) -> None:
        """Load a specific map file"""
        map_path = asset_path("tilemaps", f"{map_name}.tmx")
        self.map_data = load_pygame(map_path)

        if self.map_data is None:
            raise ValueError(f"Failed to load map: {map_name}")

        # Create sprite groups for each layer type
        self.sprite_groups[map_name] = {
            "background": pygame.sprite.Group(),
            "objects": pygame.sprite.Group(),
        }

        # Load all visible layers
        for layer in self.map_data.visible_layers:
            if hasattr(layer, "data"):
                # Determine which group to use based on layer name/properties
                group = (  # type: ignore
                    self.sprite_groups[map_name]["background"]
                    if "background" in layer.name.lower()
                    else self.sprite_groups[map_name]["objects"]
                )

                for x, y, surf in layer.tiles():
                    if surf:  # Only create tile if there's a surface
                        pos = (
                            x * self.map_data.tilewidth,
                            y * self.map_data.tileheight,
                        )
                        Tile(pos, surf, group)

        self.current_map = map_name

    def draw(self, window: Window) -> None:
        """Draw all layers in the correct order"""
        if self.current_map and self.current_map in self.sprite_groups:
            # Draw background first
            self.sprite_groups[self.current_map]["background"].draw(window.screen)  # type: ignore
            # Then draw other layers
            self.sprite_groups[self.current_map]["objects"].draw(window.screen)  # type: ignore
