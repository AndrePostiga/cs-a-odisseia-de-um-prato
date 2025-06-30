from app.pplay.sprite import Sprite
from app.core.observer import Observable


class MenuButton(Sprite, Observable):
    def __init__(self, image_file: str, x: float, y: float, action: str):
        Sprite.__init__(self, image_file)
        Observable.__init__(self)
        self.x = x
        self.y = y
        self.action = action  # Mensagem a ser enviada quando clicar
        self.is_hovered = False
        self.original_x = x
        self.original_y = y

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        return (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def update_hover_state(self, mouse_x: int, mouse_y: int) -> None:
        was_hovered = self.is_hovered
        self.is_hovered = self.is_clicked(mouse_x, mouse_y)

        if self.is_hovered and not was_hovered:
            self.x = self.original_x - 2
            self.y = self.original_y - 2
        elif not self.is_hovered and was_hovered:
            self.x = self.original_x
            self.y = self.original_y

    def on_click(self) -> None:
        self.notify_observers(self.action)
