import logging
from typing import Optional
from app.pplay.window import Window
from app.pplay.sound import Sound
from app.core.level_slider import LevelSlider
from app.core.game_state import GameState
from app.ui.main_menu import MainMenu
from app.ui.pause_menu import PauseMenu
from app.core.observer import Observer
from app.seedwork.path_helper import asset_path
from app.core.end_game_state import EndGameState


class Game(Observer):
    def __init__(self, window: Window):
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.running = True
        self.current_state = GameState.MENU
        self.logger.info("Game initialized")

        self.game_music = Sound(asset_path("musics", "game.mp3"))
        self.game_music.set_volume(25)
        self.game_music.set_repeat(True)

        # Menus
        self.menu = MainMenu(window)
        self.pause_menu = PauseMenu(window)

        # Observers
        self.menu.add_observer(self)
        self.pause_menu.add_observer(self)

        # Levels
        self.level_slider: Optional[LevelSlider] = None

        # End Game
        self.end_game_state: Optional[EndGameState] = None

        # Pause
        self.esc_pressed = False

    def on_notification(self, message: str) -> None:
        self.logger.info(f"Game received notification: {message}")

        if message == "start_game":
            self._start_game()
        elif message == "continue_game":
            self.current_state = GameState.PLAYING
            if not self.game_music.is_playing():
                self.game_music.play()
            self.logger.info("Game resumed from menu")
        elif message == "main_menu":
            self.game_music.stop()
            self.menu.start_music()
            self.current_state = GameState.MENU
            self.level_slider = None
            self.logger.info("Returned to main menu")
        elif message == "game_won":
            self.game_music.stop()
            if self.level_slider:
                rescued_characters = self.level_slider.rescued_characters
                self.end_game_state = EndGameState(self.window, rescued_characters)
                self.end_game_state.add_observer(self)
                self.current_state = GameState.GAME_WON
                self.level_slider = None
                self.logger.info("Game won!")
        elif message == "RESTART_GAME":
            self.end_game_state = None
            self.current_state = GameState.MENU
            self.menu.start_music()
            self.logger.info("Restarting game, returning to main menu.")
        elif message == "EXIT_GAME":
            self.running = False
            self.logger.info("Exiting game.")

    def _start_game(self) -> None:
        self.logger.info("Starting game")
        self.menu.stop_music()
        self.game_music.play()

        self.window.set_background_color((0, 0, 0))
        self.level_slider = LevelSlider(self.window)
        self.level_slider.add_observer(self)

        self.current_state = GameState.PLAYING

    def _handle_pause_input(self) -> None:
        keyboard = self.window.get_keyboard()
        esc_currently_pressed = keyboard.key_pressed("ESC")

        if esc_currently_pressed and not self.esc_pressed:
            if self.current_state == GameState.PLAYING:
                self.current_state = GameState.PAUSED
                self.game_music.pause()
                self.logger.info("Game paused")
            elif self.current_state == GameState.PAUSED:
                self.current_state = GameState.PLAYING
                self.game_music.unpause()
                self.logger.info("Game resumed")

        self.esc_pressed = esc_currently_pressed

    def run(self) -> None:
        self.logger.info("Starting game loop")
        self.menu.start_music()

        while self.running:
            delta_time = self.window.delta_time()

            if self.current_state == GameState.MENU:
                self.menu.update(delta_time)
                self.menu.draw()
            elif self.current_state == GameState.GAME_WON:
                if self.end_game_state:
                    self.end_game_state.update(delta_time)
                    self.end_game_state.draw()
            elif self.current_state == GameState.PLAYING:
                if self.level_slider:
                    self._handle_pause_input()
                    self.window.set_background_color((0, 0, 0))
                    self.level_slider.update(delta_time)
                    # A verificação é necessária porque o update pode ter mudado o estado
                    if self.current_state == GameState.PLAYING:
                        self.level_slider.draw()
            elif self.current_state == GameState.PAUSED:
                if self.level_slider:
                    self._handle_pause_input()
                    self.window.set_background_color((0, 0, 0))
                    self.level_slider.draw()
                    self.pause_menu.update(delta_time)
                    self.pause_menu.draw()

            self.window.update()
