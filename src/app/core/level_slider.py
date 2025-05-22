import logging
from app.core.level import Level
from app.core.observer import Observer
from app.pplay.window import Window
from app.entities.potato import Potato


class LevelSlider(Observer):
    def __init__(self, window: Window, start_level: int = 1):
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.max_level = 10
        self.min_level = 1
        self.current_level_num = start_level

        # Criar personagem principal
        self.main_character = Potato(300, 300)
        self.main_character.add_observer(self)

        # Carregar apenas o nível atual
        self.current_level = self._create_level(self.current_level_num)
        self._add_player_to_current_level()

    def _create_level(self, level_num: int) -> Level:
        self.logger.info(f"Carregando nível {level_num}")
        return Level(self.window, level_num)

    def _add_player_to_current_level(self) -> None:
        self.logger.info(
            f"Adicionando personagem principal ao nível {self.current_level_num}"
        )
        self.current_level.set_main_character(self.main_character)

    def on_notification(self, message: str) -> None:
        self.logger.info(f"Recebida notificação: {message}")
        if message == "hit_top_wall":
            self.slide_next()
        elif message == "hit_bottom_wall":
            self.slide_previous()

    def slide_next(self) -> None:
        next_level_num = self.current_level_num + 1
        if next_level_num > self.max_level:
            self.logger.info("Já está no último nível, não pode avançar.")
            return

        # Guardar velocidades do jogador para manter o movimento
        vx, vy = self.main_character.vx, self.main_character.vy

        self.logger.info(f"Avançando para o nível {next_level_num}")
        self.current_level_num = next_level_num

        # Criar nova instância do nível
        self.current_level = self._create_level(self.current_level_num)

        # Posicionar o jogador na base do novo nível
        self.main_character.y = self.window.height - self.main_character.height

        # Manter as velocidades para continuar o movimento
        self.main_character.vx, self.main_character.vy = vx, vy

        self.logger.info(f"Posição do jogador ajustada para y={self.main_character.y}")
        self._add_player_to_current_level()

    def slide_previous(self) -> None:
        prev_level_num = self.current_level_num - 1
        if prev_level_num < self.min_level:
            self.logger.info("Já está no primeiro nível, não pode retroceder.")
            return

        # Guardar velocidades do jogador para manter o movimento
        vx, vy = self.main_character.vx, self.main_character.vy

        self.logger.info(f"Retornando para o nível {prev_level_num}")
        self.current_level_num = prev_level_num

        # Criar nova instância do nível
        self.current_level = self._create_level(self.current_level_num)

        # Posicionar o jogador no topo do novo nível
        self.main_character.y = 0

        # Manter as velocidades para continuar o movimento
        self.main_character.vx, self.main_character.vy = vx, vy

        self.logger.info("Posição do jogador ajustada para y=0")
        self._add_player_to_current_level()

    def update(self, delta_time: float) -> None:
        self.current_level.update(delta_time)

    def draw(self, window: Window) -> None:
        self.current_level.draw()
