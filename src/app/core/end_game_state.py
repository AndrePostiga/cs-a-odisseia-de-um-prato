import random
import logging
from typing import Set, List
import pygame
from app.pplay.window import Window
from app.pplay.gameimage import GameImage
from app.ui.menu_button import MenuButton
from app.core.observer import Observable, Observer
from app.entities.jumping_character import JumpingCharacter
from app.pplay.sound import Sound
from app.seedwork.path_helper import asset_path


class EndGameState(Observable, Observer):
    def __init__(
        self, window: Window, rescued_characters: Set[str], initial_volume: int = 5
    ):
        super().__init__()
        self.window = window
        self.logger = logging.getLogger(__name__)
        self.background = GameImage(asset_path("images", "fim.png"))

        self.menu_music = Sound(asset_path("musics", "fim.mp3"))
        self.menu_music.set_volume(initial_volume)
        self.menu_music.set_repeat(True)

        self.main_menu_button = MenuButton(
            asset_path("images", "main_menu_button.png"),
            0,
            50,
            "main_menu",
        )
        # Centraliza o botão e corrige a posição original para o hover
        self.main_menu_button.x = (
            self.window.width / 2 - self.main_menu_button.width / 2
        )
        self.main_menu_button.original_x = self.main_menu_button.x

        self.main_menu_button.add_observer(self)

        self.characters: List[JumpingCharacter] = []
        self.rescued_text_info: dict | None = None
        self._create_characters(rescued_characters)

    def start_music(self) -> None:
        if not self.menu_music.is_playing():
            self.menu_music.play()
            self.logger.info("End music started")

    def stop_music(self) -> None:
        self.menu_music.stop()
        self.logger.info("End music stopped")

    def _create_characters(self, rescued_characters: Set[str]):
        all_possible_friends = {"butter", "cheese", "dried_meat", "milk"}
        if len(rescued_characters) < len(all_possible_friends):
            text = f"Amigos resgatados: {len(rescued_characters)}/{len(all_possible_friends)}"
            font = pygame.font.SysFont("Segoe UI", 36, bold=True)
            text_surface = font.render(text, True, (255, 255, 255))
            x = self.window.width / 2 - text_surface.get_width() / 2
            y = self.window.height - 250
            self.rescued_text_info = {
                "text": text,
                "x": x,
                "y": y,
                "size": 36,
                "color": (255, 255, 255),
                "font_name": "Arial",
                "bold": True,
            }

        # Cria a lista de personagens a serem exibidos (apenas os resgatados + batata)
        characters_to_create = [
            JumpingCharacter(
                asset_path("images", "characters", "potato", "idle", "1.png"), 0, 0
            )
        ]
        for name in rescued_characters:
            characters_to_create.append(
                JumpingCharacter(
                    asset_path("images", "characters", name, "idle", "7.png"), 0, 0
                )
            )

        # Calcula a largura total e a posição inicial para centralizar
        spacing = 20
        total_width = sum(char.sprite.width for char in characters_to_create)
        total_width += spacing * (len(characters_to_create) - 1)
        start_x = (self.window.width - total_width) / 2

        # Define a posição final de cada personagem
        current_x = start_x
        for character in characters_to_create:
            character.transform.x = current_x
            character.transform.y = self.window.height - 150
            self.characters.append(character)
            current_x += character.sprite.width + spacing

    def update(self, delta_time: float):
        for char in self.characters:
            char.update(delta_time)
            # Colisão com a borda inferior
            if char.transform.y >= self.window.height - char.sprite.height:
                char.transform.y = self.window.height - char.sprite.height
                char.movement.vy = -random.randint(500, 700)

        mouse = self.window.get_mouse()
        mouse_x, mouse_y = mouse.get_position()

        self.main_menu_button.update_hover_state(mouse_x, mouse_y)

        if mouse.is_button_pressed(1):
            self.stop_music()
            if self.main_menu_button.is_hovered:
                self.main_menu_button.on_click()

    def draw(self):
        self.background.draw()
        if self.rescued_text_info:
            self.window.draw_text(**self.rescued_text_info)
        for char in self.characters:
            char.draw()
        self.main_menu_button.draw()

    def on_notification(self, message: str) -> None:
        self.notify_observers(message)

    def on_exit(self):
        self.logger.info("Saindo do EndGameState.")
