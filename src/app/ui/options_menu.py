import pygame
from app.pplay.window import Window
from app.core.observer import Observable, Observer
from app.pplay.sprite import Sprite
from app.seedwork.path_helper import asset_path

class OptionsMenu(Observer, Observable):
    def __init__(self, window: Window, initial_volume: int = 5):
        Observable.__init__(self)
        self.window = window
        self.volume = initial_volume  # 0 a 100
        self.slider_rect = pygame.Rect(window.width // 2 - 150, window.height // 2, 300, 10)
        self.dragging = False

    def on_notification(self, message: str) -> None:
        pass

    def update(self, delta_time: float):
        mouse = self.window.get_mouse()
        mouse_x, mouse_y = mouse.get_position()
        mouse_pressed = mouse.is_button_pressed(mouse.BUTTON_LEFT)

        if self.slider_rect.collidepoint(mouse_x, mouse_y) and mouse_pressed:
            self.dragging = True
        if not mouse_pressed:
            self.dragging = False

        if self.dragging:
            rel_x = max(0, min(mouse_x - self.slider_rect.x, self.slider_rect.width))
            self.volume = int((rel_x / self.slider_rect.width) * 100)
            self.notify_observers(("set_volume", self.volume))

        # Botão de voltar
        if mouse_pressed:
            if self.window.width // 2 - 60 < mouse_x < self.window.width // 2 + 60 and \
               self.window.height // 2 + 50 < mouse_y < self.window.height // 2 + 100:
                self.notify_observers("back_from_options")

    def draw(self):
        screen = self.window.get_screen()
        # Overlay preto semi-transparente
        overlay_surface = pygame.Surface((self.window.width, self.window.height))
        overlay_surface.fill((0, 0, 0))
        overlay_surface.set_alpha(180)
        screen.blit(overlay_surface, (0, 0))

        font = pygame.font.SysFont("Segoe UI", 36, bold=True)
        # Título
        text = font.render("VOLUME", True, (255, 255, 255))
        screen.blit(text, (self.window.width // 2 - text.get_width() // 2, self.window.height // 2 - 100))
        # Slider
        pygame.draw.rect(screen, (200, 200, 200), self.slider_rect)
        handle_x = self.slider_rect.x + int(self.volume / 100 * self.slider_rect.width)
        pygame.draw.circle(screen, (100, 200, 255), (handle_x, self.slider_rect.y + 5), 15)
        # Valor do volume
        value_text = font.render(f"{self.volume}", True, (255, 255, 255))
        screen.blit(value_text, (self.window.width // 2 - value_text.get_width() // 2, self.window.height // 2 - 60))
        # Botão voltar
        pygame.draw.rect(screen, (100, 100, 100), (self.window.width // 2 - 60, self.window.height // 2 + 50, 120, 50))
        back_text = font.render("Voltar", True, (255, 255, 255))
        button_x = self.window.width // 2 - 60
        button_y = self.window.height // 2 + 50
        button_width = 120
        button_height = 50
        back_text_x = button_x + (button_width - back_text.get_width()) // 2
        back_text_y = button_y + (button_height - back_text.get_height()) // 2
        screen.blit(back_text, (back_text_x, back_text_y))