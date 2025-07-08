from app.pplay.sprite import Sprite
from app.pplay.window import Window
from app.entities.potato import Potato
from app.seedwork.path_helper import asset_path


class AltitudeHUD:
    def __init__(self, window: Window):
        self.window = window
        self.is_visible = True

        try:
            self.ruler_image = Sprite(asset_path("images", "hud", "ruler.png"))
            self.icon_image = Sprite(asset_path("images", "hud", "potato_icon.png"))
        except Exception as e:
            print(
                "ERRO: Não foi possível carregar as imagens do HUD. Verifique os caminhos."
            )
            print(f"Detalhe: {e}")
            self.is_visible = False
            return

        margin = 20
        ruler_x = self.window.width - self.ruler_image.width - margin
        ruler_y = margin
        self.ruler_image.set_position(ruler_x, ruler_y)

    def update(self, main_character: Potato, current_level_num: int, max_level: int):
        if not self.is_visible:
            return

        level_height = self.window.height
        player_y_in_level = main_character.transform.y
        normalized_y_in_level = player_y_in_level / level_height

        # progresso geral
        progress_per_level = 1 / max_level
        progress_of_previous_levels = (current_level_num - 1) * progress_per_level
        progress_in_current_level = (1 - normalized_y_in_level) * progress_per_level
        total_progress = progress_of_previous_levels + progress_in_current_level

        # progresso entre 0 e 1
        progress_ratio = max(0, min(1, total_progress))

        # Mapeia a porcentagem de progresso para a posição Y na régua
        ruler_span = self.ruler_image.height - self.icon_image.height
        icon_y_offset = ruler_span * (1 - progress_ratio)

        icon_x = (
            self.ruler_image.x
            + (self.ruler_image.width / 2)
            - (self.icon_image.width / 2)
        )
        icon_y = self.ruler_image.y + icon_y_offset

        self.icon_image.set_position(icon_x, icon_y)

    def draw(self):
        """
        Desenha a régua e o ícone na tela.
        """
        if not self.is_visible:
            return

        self.ruler_image.draw()
        self.icon_image.draw()
