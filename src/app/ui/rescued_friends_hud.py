import pygame
from typing import Set
from app.pplay.window import Window
from app.seedwork.path_helper import asset_path
from app.core.observer import Observer


class RescuedFriendsHUD(Observer):
    def __init__(self, window: Window):
        self.window = window
        self.font_size = 24
        self.font_name = "Arial"
        self.text_color = (255, 255, 255)
        self.character_order = ["butter", "cheese", "dried_meat", "milk"]
        self.rescued_friends: Set[str] = set()
        self.icons = self._load_icons()
        self.gray_icons = {
            name: self._grayscale(icon) for name, icon in self.icons.items()
        }

    def on_notification(self, message: str) -> None:
        if message.startswith("rescued_"):
            character_name = message[len("rescued_"):]
            if character_name in self.character_order:
                self.rescued_friends.add(character_name)
    
    def _load_icons(self) -> dict[str, pygame.Surface]:
        icon_files = {
            "butter": "butter_icon.png",
            "cheese": "cheese_icon.png",
            "dried_meat": "dried_meat_icon.png",
            "milk": "milk_icon.png",
        }
        icons = {}
        for name, filename in icon_files.items():
            icon_path = asset_path("images", "hud", filename)
            icon = pygame.image.load(icon_path).convert_alpha()
            scaled_icon = pygame.transform.scale(icon, (48, 48))
            icons[name] = scaled_icon
        return icons

    def _grayscale(self, surface: pygame.Surface) -> pygame.Surface:
        gray_surface = surface.copy()
        for x in range(gray_surface.get_width()):
            for y in range(gray_surface.get_height()):
                r, g, b, a = gray_surface.get_at((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                gray_surface.set_at((x, y), (gray, gray, gray, a))
        return gray_surface

    def draw(self):
        if not self.window.screen:
            return

        text_content = "Amigos Resgatados"
        icon_height = 48
        space_between = 5
        total_hud_height = self.font_size + space_between + icon_height

        margin_bottom = 20
        text_x = self.window.width - 300
        text_y = self.window.height - total_hud_height - margin_bottom

        self.window.draw_text(
            text_content,
            text_x,
            text_y,
            size=self.font_size,
            font_name=self.font_name,
            color=self.text_color,
        )

        # desenha os ícones abaixo do texto
        start_x = text_x
        icon_y = text_y + self.font_size + space_between

        for i, name in enumerate(self.character_order):
            icon_to_draw = (
                self.icons[name]
                if name in self.rescued_friends
                else self.gray_icons[name]
            )
            icon_rect = icon_to_draw.get_rect(topleft=(start_x + i * 52, icon_y))
            self.window.screen.blit(icon_to_draw, icon_rect)
