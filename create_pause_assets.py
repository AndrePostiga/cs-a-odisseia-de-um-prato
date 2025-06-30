"""
Script to generate pause menu assets.
"""

import pygame
import os

# Initialize pygame
pygame.init()


def create_button_image(
    text: str,
    width: int,
    height: int,
    bg_color: tuple,
    text_color: tuple,
    filename: str,
):
    """Create a simple button image with text."""
    surface = pygame.Surface((width, height))
    surface.fill(bg_color)

    # Add border
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 3)

    # Add text
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface, text_rect)

    # Save image
    assets_dir = "/home/andrepostiga/work/cs-a-odisseia-de-um-prato/assets/images"
    image_path = os.path.join(assets_dir, filename)
    pygame.image.save(surface, image_path)
    print(f"Created: {image_path}")


def create_pause_overlay(width: int, height: int, filename: str):
    """Create a semi-transparent overlay for pause menu."""
    surface = pygame.Surface((width, height))

    # Create semi-transparent dark overlay
    surface.fill((0, 0, 0))
    surface.set_alpha(180)  # Semi-transparent

    # Save image
    assets_dir = "/home/andrepostiga/work/cs-a-odisseia-de-um-prato/assets/images"
    image_path = os.path.join(assets_dir, filename)
    pygame.image.save(surface, image_path)
    print(f"Created: {image_path}")


if __name__ == "__main__":
    # Create pause menu buttons
    create_button_image(
        "CONTINUAR", 200, 60, (100, 150, 200), (255, 255, 255), "continue_button.png"
    )
    create_button_image(
        "MENU PRINCIPAL",
        200,
        60,
        (150, 100, 200),
        (255, 255, 255),
        "main_menu_button.png",
    )
    create_button_image(
        "SAIR", 200, 60, (200, 100, 100), (255, 255, 255), "exit_button.png"
    )

    # Create pause overlay (1920x1080 for 1080p)
    create_pause_overlay(1920, 1080, "pause_overlay.png")

    pygame.quit()
    print("All pause menu assets created successfully!")
