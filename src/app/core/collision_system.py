import pygame
from typing import List
from app.entities.tile import Tile
from app.components.transform import Transform
from app.components.movement import Movement


class CollisionHandler:
    def handle_collisions(
        self, transform: Transform, movement: Movement, tiles: List[Tile], dt: float
    ):
        # Movimento horizontal
        transform.x += movement.vx * dt
        transform.update_rect()

        for tile in tiles:
            if transform.rect.colliderect(tile.rect):
                # Colidiu se movendo para a direita
                if movement.vx > 0:
                    transform.rect.right = tile.rect.left
                    movement.vx = 0
                # Colidiu se movendo para a esquerda
                elif movement.vx < 0:
                    transform.rect.left = tile.rect.right
                    movement.vx = 0
                transform.x = transform.rect.x  # Atualiza a posição do transform

        # Movimento vertical
        transform.y += movement.vy * dt
        transform.update_rect()

        for tile in tiles:
            if transform.rect.colliderect(tile.rect):
                # Colidiu caindo
                if movement.vy > 0:
                    transform.rect.bottom = tile.rect.top
                    movement.vy = 0
                # Colidiu pulando
                elif movement.vy < 0:
                    transform.rect.top = tile.rect.bottom
                    movement.vy = 0
                transform.y = transform.rect.y  # Atualiza a posição do transform

    def check_on_ground(self, transform: Transform, tiles: List[Tile]) -> bool:
        # cria um retângulo de 1 pixel de altura logo abaixo do personagem
        ground_check_rect = pygame.Rect(
            transform.rect.x, transform.rect.bottom, transform.rect.width, 1
        )
        for tile in tiles:
            if ground_check_rect.colliderect(tile.rect):
                return True
        return False

    def check_bounds(
        self,
        transform: Transform,
        movement: Movement,
        window_width: int,
        window_height: int,
    ):
        boundary_hit = None

        # Borda de cima (para transição de nível)
        if transform.y < 0:
            boundary_hit = "hit_top_wall"

        # Borda de baixo (para transição de nível)
        elif transform.y + transform.height > window_height:
            boundary_hit = "hit_bottom_wall"

        # Bordas laterais (impede o jogador de sair da tela)
        if transform.x < 0:
            transform.x = 0
            movement.vx = 0
        elif transform.x + transform.width > window_width:
            transform.x = float(window_width - transform.width)
            movement.vx = 0

        transform.update_rect()
        return boundary_hit
