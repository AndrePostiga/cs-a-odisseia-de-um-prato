import logging
import pygame
from app.pplay.window import Window
from app.pplay.sprite import Sprite
from app.ui.menu_button import MenuButton
from app.seedwork.path_helper import asset_path
from app.core.observer import Observer, Observable


class PauseMenu(Observer, Observable):
    def __init__(self, window: Window):
        Observable.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.window = window

        # Semi-transparent overlay
        self.overlay = Sprite(asset_path("images", "pause_overlay.png"))
        self.overlay.x = 0
        self.overlay.y = 0
        # Scale overlay to cover entire screen
        self.overlay.width = window.width
        self.overlay.height = window.height

        # Calculate button positions (centered)
        button_width = 200
        button_height = 60
        button_spacing = 80

        center_x = (window.width - button_width) // 2
        start_y = (window.height - (3 * button_height + 2 * button_spacing)) // 2

        # Store positions for later use
        self.center_x = center_x
        self.start_y = start_y

        # Create buttons with actions
        self.continue_button = MenuButton(
            asset_path("images", "continue_button.png"),
            center_x,
            start_y,
            "continue_game",
        )

        self.main_menu_button = MenuButton(
            asset_path("images", "main_menu_button.png"),
            center_x,
            start_y + button_height + button_spacing,
            "main_menu",
        )

        self.exit_button = MenuButton(
            asset_path("images", "exit_button.png"),
            center_x,
            start_y + 2 * (button_height + button_spacing),
            "exit_game",
        )

        self.continue_button.add_observer(self)
        self.main_menu_button.add_observer(self)
        self.exit_button.add_observer(self)

        self.buttons = [self.continue_button, self.main_menu_button, self.exit_button]
        self.mouse_clicked = False

        self.logger.info("PauseMenu initialized")

    def on_notification(self, message: str) -> None:
        self.logger.info(f"PauseMenu received notification: {message}")

        if message == "continue_game":
            self.logger.info("Continue button clicked")
            self.notify_observers("continue_game")
        elif message == "main_menu":
            self.logger.info("Main menu button clicked")
            self.notify_observers("main_menu")
        elif message == "exit_game":
            self.logger.info("Exit button clicked")
            self.window.close()

    def update(self, delta_time: float) -> None:
        mouse = self.window.get_mouse()
        mouse_pos = mouse.get_position()
        mouse_x, mouse_y = mouse_pos

        for button in self.buttons:
            button.update_hover_state(mouse_x, mouse_y)

        mouse_pressed = mouse.is_button_pressed(mouse.BUTTON_LEFT)

        if mouse_pressed and not self.mouse_clicked:
            for button in self.buttons:
                if button.is_clicked(mouse_x, mouse_y):
                    button.on_click()
                    break

        self.mouse_clicked = mouse_pressed

    def draw(self) -> None:
        # Draw semi-transparent overlay manually if sprite doesn't work
        overlay_surface = pygame.Surface((self.window.width, self.window.height))
        overlay_surface.fill((0, 0, 0))
        overlay_surface.set_alpha(180)  # Semi-transparent
        self.window.get_screen().blit(overlay_surface, (0, 0))

        # Draw buttons next (middle layer)
        for button in self.buttons:
            button.draw()

        # Draw title last (foreground) so it appears on top
        title_text = "JOGO PAUSADO"
        # Calculate center position for title more precisely
        # Estimate text width: roughly 12 pixels per character at size 48
        text_width = len(title_text) * 28  # More accurate estimation for size 48
        title_x = (self.window.width - text_width) // 2  # Perfect centering
        title_y = self.start_y - 100  # Position above buttons with proper spacing
        self.window.draw_text(
            title_text,
            title_x,
            title_y,
            size=48,
            color=(255, 255, 255),
            font_name="Arial",
            bold=True,
        )
