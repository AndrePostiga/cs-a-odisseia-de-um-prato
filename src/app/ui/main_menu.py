import logging
from app.pplay.window import Window
from app.pplay.sprite import Sprite
from app.ui.menu_button import MenuButton
from app.seedwork.path_helper import asset_path
from app.core.observer import Observer, Observable


class MainMenu(Observer, Observable):
    def __init__(self, window: Window):
        Observable.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.window = window

        # Background
        self.background = Sprite(asset_path("images", "menu_background.png"))
        self.background.x = 0
        self.background.y = 0

        # Buttons
        button_width = 200
        button_height = 60
        button_spacing = 80

        center_x = (window.width - button_width) // 2
        start_y = (window.height - (2 * button_height + button_spacing)) // 2

        self.play_button = MenuButton(
            asset_path("images", "play_button.png"),
            center_x,
            start_y,
            "start_game",  # Action identifier
        )

        self.quit_button = MenuButton(
            asset_path("images", "quit_button.png"),
            center_x,
            start_y + button_height + button_spacing,
            "quit_game",  # Action identifier
        )

        # Register as observer for button events
        self.play_button.add_observer(self)
        self.quit_button.add_observer(self)

        self.buttons = [self.play_button, self.quit_button]
        self.mouse_clicked = False

        self.logger.info("Main menu initialized")

    def on_notification(self, message: str) -> None:
        """Handle notifications from button clicks."""
        self.logger.info(f"MainMenu received notification: {message}")

        if message == "start_game":
            self.logger.info("Play button clicked")
            # Notify game observers about the start game request
            self.notify_observers("start_game")
        elif message == "quit_game":
            self.logger.info("Quit button clicked")
            self.window.close()

    def update(self, delta_time: float) -> None:
        """Update menu logic."""
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
        """Draw the menu."""
        # Draw background
        self.background.draw()

        # Draw buttons
        for button in self.buttons:
            button.draw()
