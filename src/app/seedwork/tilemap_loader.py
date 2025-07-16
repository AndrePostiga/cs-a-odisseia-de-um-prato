# type: ignore
from typing import List, Tuple
from pygame.sprite import Group
from app.seedwork.path_helper import asset_path
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer, TiledObjectGroup, TiledImageLayer, TiledMap
from app.entities.tile import Tile
from app.entities.background_tile import BackgroundTile
from app.core.tilemap_group import TilemapGroup
import logging

logger = logging.getLogger(__name__)


def load_tilemap_groups(map_name: str) -> List[Tuple[TilemapGroup, Group]]:
    map_path = asset_path("tilemaps", f"{map_name}.tmx")
    logger.info(f"Loading tilemap from: {map_path}")
    map_data = load_pygame(map_path)

    ordered_groups: List[Tuple[TilemapGroup, Group]] = []

    for layer in map_data.visible_layers:
        if isinstance(layer, TiledTileLayer):
            group_key, group = _process_tile_layer(layer, map_data)
            ordered_groups.append((group_key, group))
        elif isinstance(layer, TiledObjectGroup):
            group = _process_object_group(layer, map_data)
            ordered_groups.append((TilemapGroup.SCENERY_OBJECT, group))
        elif isinstance(layer, TiledImageLayer):
            group = _process_image_layer(layer)
            ordered_groups.append((TilemapGroup.BACKGROUND, group))

    return ordered_groups


def _process_tile_layer(
    layer: TiledTileLayer, map_data: TiledMap
) -> Tuple[TilemapGroup, Group]:
    layer_type = layer.properties.get("type")

    # Determina o tipo de grupo baseado nas propriedades da camada
    if layer_type == "interactive-block":
        group_key = TilemapGroup.INTERACTIVE_BLOCK
    else:
        group_key = TilemapGroup.SCENERY_BLOCK

    group = Group()
    for x, y, surf in layer.tiles():
        if surf:
            tile = Tile(x * map_data.tilewidth, y * map_data.tileheight, surf)
            group.add(tile)

    return group_key, group


def _process_object_group(layer: TiledObjectGroup, map_data: TiledMap) -> Group:
    group = Group()

    for obj in layer:
        if getattr(obj, "gid", None):
            surf = map_data.get_tile_image_by_gid(obj.gid)
            if surf:
                y_aligned = obj.y - surf.get_height()
                tile = Tile(obj.x, y_aligned, surf)
                group.add(tile)

    return group


def _process_image_layer(layer: TiledImageLayer) -> Group:
    group = Group()
    if layer.image:
        background_tile = BackgroundTile(layer.image)
        group.add(background_tile)

    return group
