import pygame
from typing import List
from app.entities.tile import Tile
from app.components.transform import Transform
from app.components.movement import Movement


class CollisionHandler:
    def __init__(self):
        # Maximum distance to move in one frame to prevent tunneling
        self.max_move_distance = 16.0

    def handle_tile_collisions(
        self, transform: Transform, movement: Movement, tiles: List[Tile]
    ):
        """Handle collisions with tiles."""
        if not tiles:
            movement.is_on_ground = False
            return

        # Handle vertical collisions first (more important for platformers)
        if movement.vy != 0:
            for tile in tiles:
                if transform.rect.colliderect(tile.rect):
                    self._resolve_vertical_collision(transform, movement, tile)
                    # If we resolved a vertical collision, update rect and check again
                    break  # Only handle one vertical collision per frame

        # Then handle horizontal collisions
        if movement.vx != 0:
            for tile in tiles:
                if transform.rect.colliderect(tile.rect):
                    self._resolve_horizontal_collision(transform, movement, tile)
                    # If we resolved a horizontal collision, update rect and check again
                    break  # Only handle one horizontal collision per frame

        # Safety check: if player is still inside a tile after collision resolution,
        # move them back to a safe position
        for tile in tiles:
            if transform.rect.colliderect(tile.rect):
                # Find the smallest displacement to get out of the tile
                overlap_left = transform.rect.right - tile.rect.left
                overlap_right = tile.rect.right - transform.rect.left
                overlap_top = transform.rect.bottom - tile.rect.top
                overlap_bottom = tile.rect.bottom - transform.rect.top

                # Choose the smallest displacement
                min_displacement = min(
                    overlap_left, overlap_right, overlap_top, overlap_bottom
                )

                if min_displacement == overlap_left:
                    transform.x = float(tile.rect.left - transform.width)
                    movement.vx = 0.0
                elif min_displacement == overlap_right:
                    transform.x = float(tile.rect.right)
                    movement.vx = 0.0
                elif min_displacement == overlap_top:
                    transform.y = float(tile.rect.top - transform.height)
                    movement.vy = 0.0
                elif min_displacement == overlap_bottom:
                    transform.y = float(tile.rect.bottom)
                    movement.vy = 0.0

                transform.update_rect()
                break  # Only resolve one overlap per frame

        # After collision resolution, check if player is actually on ground
        # This ensures proper falling when walking off platforms
        movement.is_on_ground = self.is_on_ground(transform, tiles)

    def _resolve_vertical_collision(
        self, transform: Transform, movement: Movement, tile: Tile
    ):
        """Resolve vertical collision with a single tile."""
        # Landing on top of tile (falling down)
        if (
            movement.vy > 0
            and transform.rect.bottom > tile.rect.top
            and transform.rect.top < tile.rect.top
            and not (
                transform.rect.right <= tile.rect.left
                or transform.rect.left >= tile.rect.right
            )
        ):
            transform.y = float(tile.rect.top - transform.height)
            movement.vy = 0.0
            transform.update_rect()

        # Hitting ceiling (moving up)
        elif (
            movement.vy < 0
            and transform.rect.top < tile.rect.bottom
            and transform.rect.bottom > tile.rect.bottom
            and not (
                transform.rect.right <= tile.rect.left
                or transform.rect.left >= tile.rect.right
            )
        ):
            transform.y = float(tile.rect.bottom)
            movement.vy = 0.0
            transform.update_rect()

    def _resolve_horizontal_collision(
        self, transform: Transform, movement: Movement, tile: Tile
    ):
        """Resolve horizontal collision with a single tile."""
        # Hit right wall (moving right)
        if (
            movement.vx > 0
            and transform.rect.right > tile.rect.left
            and transform.rect.left < tile.rect.left
            and not (
                transform.rect.bottom <= tile.rect.top
                or transform.rect.top >= tile.rect.bottom
            )
        ):
            transform.x = float(tile.rect.left - transform.width)
            movement.vx = 0.0
            transform.update_rect()

        # Hit left wall (moving left)
        elif (
            movement.vx < 0
            and transform.rect.left < tile.rect.right
            and transform.rect.right > tile.rect.right
            and not (
                transform.rect.bottom <= tile.rect.top
                or transform.rect.top >= tile.rect.bottom
            )
        ):
            transform.x = float(tile.rect.right)
            movement.vx = 0.0
            transform.update_rect()

    def _resolve_tile_collision(
        self, transform: Transform, movement: Movement, tile: Tile
    ):
        """Resolve collision with a single tile."""
        # Landing on top of tile
        if (
            movement.vy > 0
            and transform.rect.bottom >= tile.rect.top
            and transform.rect.top < tile.rect.top
        ):
            transform.y = float(tile.rect.top - transform.height)
            movement.vy = 0.0
            # Don't set is_on_ground here - it will be determined in handle_tile_collisions
            transform.update_rect()

        # Hitting ceiling
        elif (
            movement.vy < 0
            and transform.rect.top <= tile.rect.bottom
            and transform.rect.bottom > tile.rect.bottom
        ):
            transform.y = float(tile.rect.bottom)
            movement.vy = 0.0
            transform.update_rect()

        # Hit right wall (moving right)
        elif (
            movement.vx > 0
            and transform.rect.right >= tile.rect.left
            and transform.rect.left < tile.rect.left
        ):
            transform.x = float(tile.rect.left - transform.width)
            movement.vx = 0.0
            transform.update_rect()

        # Hit left wall (moving left)
        elif (
            movement.vx < 0
            and transform.rect.left <= tile.rect.right
            and transform.rect.right > tile.rect.right
        ):
            transform.x = float(tile.rect.right)
            movement.vx = 0.0
            transform.update_rect()

    def check_bounds(
        self,
        transform: Transform,
        movement: Movement,
        window_width: int,
        window_height: int,
    ):
        """Check and handle window boundary collisions. Returns boundary hit information."""
        boundary_hit = None

        # Top boundary - just detect, don't modify position or velocity
        if transform.y < 0:
            boundary_hit = "hit_top_wall"

        # Bottom boundary - just detect, don't modify position or velocity
        elif transform.y + transform.height > window_height:
            boundary_hit = "hit_bottom_wall"

        # Left boundary - still handle these as normal since they don't trigger level transitions
        if transform.x < 0:
            transform.x = 0.0
            movement.vx = 0.0
            transform.update_rect()

        # Right boundary - still handle these as normal since they don't trigger level transitions
        elif transform.x + transform.width > window_width:
            transform.x = float(window_width - transform.width)
            movement.vx = 0.0
            transform.update_rect()

        return boundary_hit

    def is_on_ground(self, transform: Transform, tiles: List[Tile]) -> bool:
        """Check if the player is standing on solid ground."""
        if not tiles:
            return False

        # Create a small rectangle just below the player's feet to check for ground
        ground_check_rect = pygame.Rect(
            int(transform.x + 1),  # Slightly inset to avoid edge cases
            int(transform.y + transform.height),  # Just below the player
            int(transform.width - 2),  # Slightly narrower
            2,  # Small height for the check
        )

        # Check if any tile intersects with this ground check area
        for tile in tiles:
            if ground_check_rect.colliderect(tile.rect):
                return True

        return False

    def _move_and_check_collisions(
        self,
        transform: Transform,
        movement: Movement,
        tiles: List[Tile],
        dx: float,
        dy: float,
    ) -> tuple[bool, bool]:
        """Move step by step and check for collisions. Returns (hit_horizontal, hit_vertical)."""
        hit_horizontal = False
        hit_vertical = False

        # Calculate number of steps needed
        steps = max(1, int(max(abs(dx), abs(dy)) / self.max_move_distance) + 1)
        step_x = dx / steps
        step_y = dy / steps

        for step in range(steps):
            # Move horizontally first
            if step_x != 0:
                transform.x += step_x
                transform.update_rect()

                # Check for horizontal collisions
                for tile in tiles:
                    if transform.rect.colliderect(tile.rect):
                        # Undo horizontal movement
                        transform.x -= step_x
                        transform.update_rect()
                        movement.vx = 0.0
                        hit_horizontal = True
                        break

            # Then move vertically
            if step_y != 0 and not hit_horizontal:
                transform.y += step_y
                transform.update_rect()

                # Check for vertical collisions
                for tile in tiles:
                    if transform.rect.colliderect(tile.rect):
                        # Undo vertical movement
                        transform.y -= step_y
                        transform.update_rect()
                        movement.vy = 0.0
                        hit_vertical = True
                        break

            # If we hit something, stop moving
            if hit_horizontal or hit_vertical:
                break

        return hit_horizontal, hit_vertical

    def safe_move(
        self,
        transform: Transform,
        movement: Movement,
        dx: float,
        dy: float,
        tiles: List[Tile],
    ) -> None:
        """Safely move the character step by step to prevent tunneling."""
        # Store original ground state to track changes
        was_on_ground = movement.is_on_ground

        # Calculate maximum safe move distance per step
        max_step = 8.0  # Smaller than tile size to prevent tunneling

        # Calculate number of steps needed
        distance = max(abs(dx), abs(dy))
        steps = max(1, int(distance / max_step) + 1)

        step_x = dx / steps if steps > 0 else 0
        step_y = dy / steps if steps > 0 else 0

        # Move step by step
        for step in range(steps):
            # Try horizontal movement first
            if step_x != 0:
                transform.x += step_x
                transform.update_rect()

                # Check for horizontal collisions
                for tile in tiles:
                    if transform.rect.colliderect(tile.rect):
                        # Undo movement and resolve collision
                        transform.x -= step_x
                        transform.update_rect()
                        self._resolve_horizontal_collision(transform, movement, tile)
                        break

            # Then try vertical movement
            if step_y != 0:
                transform.y += step_y
                transform.update_rect()

                # Check for vertical collisions
                for tile in tiles:
                    if transform.rect.colliderect(tile.rect):
                        # Undo movement and resolve collision
                        transform.y -= step_y
                        transform.update_rect()
                        self._resolve_vertical_collision(transform, movement, tile)
                        break

        # Final safety check: if still inside a tile, use emergency displacement
        for tile in tiles:
            if transform.rect.colliderect(tile.rect):
                self._emergency_displacement(transform, movement, tile)
                break

        # Update ground state
        movement.is_on_ground = self.is_on_ground(transform, tiles)

        # Debug ground state changes
        if was_on_ground != movement.is_on_ground:
            print(
                f"Ground state changed: was_on_ground={was_on_ground}, is_on_ground={movement.is_on_ground}"
            )

    def _emergency_displacement(
        self, transform: Transform, movement: Movement, tile: Tile
    ) -> None:
        """Emergency displacement when player is stuck inside a tile."""
        # Calculate overlaps
        overlap_left = transform.rect.right - tile.rect.left
        overlap_right = tile.rect.right - transform.rect.left
        overlap_top = transform.rect.bottom - tile.rect.top
        overlap_bottom = tile.rect.bottom - transform.rect.top

        # Find smallest displacement
        min_displacement = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_displacement == overlap_left:
            transform.x = float(tile.rect.left - transform.width)
            movement.vx = 0.0
        elif min_displacement == overlap_right:
            transform.x = float(tile.rect.right)
            movement.vx = 0.0
        elif min_displacement == overlap_top:
            transform.y = float(tile.rect.top - transform.height)
            movement.vy = 0.0
        elif min_displacement == overlap_bottom:
            transform.y = float(tile.rect.bottom)
            movement.vy = 0.0

        transform.update_rect()
