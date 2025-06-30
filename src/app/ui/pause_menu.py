import logging
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

        # Calculate button positions (centered)
        button_width = 200
        button_height = 60
        button_spacing = 80

        center_x = (window.width - button_width) // 2
        start_y = (window.height - (3 * button_height + 2 * button_spacing)) // 2

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

        # Register as observer for button events
        self.continue_button.add_observer(self)
        self.main_menu_button.add_observer(self)
        self.exit_button.add_observer(self)

        self.buttons = [self.continue_button, self.main_menu_button, self.exit_button]
        self.mouse_clicked = False

        self.logger.info("PauseMenu initialized")

    def on_notification(self, message: str) -> None:
        """Handle notifications from button clicks."""
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
        """Update pause menu logic."""
        mouse = self.window.get_mouse()
        mouse_pos = mouse.get_position()
        mouse_x, mouse_y = mouse_pos

        # Update hover states for all buttons
        for button in self.buttons:
            button.update_hover_state(mouse_x, mouse_y)

        # Handle mouse clicks
        mouse_pressed = mouse.is_button_pressed(mouse.BUTTON_LEFT)

        if mouse_pressed and not self.mouse_clicked:
            # Mouse was just pressed
            for button in self.buttons:
                if button.is_clicked(mouse_x, mouse_y):
                    button.on_click()
                    break

        self.mouse_clicked = mouse_pressed

    def draw(self) -> None:
        """Draw the pause menu."""
        # Draw semi-transparent overlay
        self.overlay.draw()

        # Draw pause title
        title_text = "JOGO PAUSADO"
        title_x = self.window.width // 2 - 120  # Rough centering
        title_y = self.window.height // 2 - 150
        self.window.draw_text(
            title_text,
            title_x,
            title_y,
            size=48,
            color=(255, 255, 255),
            font_name="Arial",
            bold=True,
        )

        # Draw buttons
        for button in self.buttons:
            button.draw()
