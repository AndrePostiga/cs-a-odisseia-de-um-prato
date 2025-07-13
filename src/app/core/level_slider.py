import logging
from typing import Set
from app.core.level import Level
from app.core.observer import Observer, Observable
from app.pplay.window import Window
from app.entities.potato import Potato
from app.ui.altitude_hud import AltitudeHUD
from app.ui.rescued_friends_hud import RescuedFriendsHUD


class LevelSlider(Observer, Observable):
    def __init__(self, window: Window, start_level: int = 1):
        Observable.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.max_level = 8
        self.min_level = 1
        self.current_level_num = start_level
        self.rescued_characters: Set[str] = set()
        self.ended = False

        # Criar personagem principal
        self.main_character = Potato(900, 600)
        self.main_character.add_observer(self)

        # Carregar apenas o nível atual
        self.current_level = self._create_level(self.current_level_num)
        self._add_player_to_current_level()

        # HUD
        self.altitude_hud = AltitudeHUD(self.window)
        self.rescued_friends_hud = RescuedFriendsHUD(self.window)
        self.main_character.add_observer(self.rescued_friends_hud)

    def _create_level(self, level_num: int) -> Level:
        self.logger.info(f"Carregando nível {level_num}")
        return Level(self.window, level_num, self.rescued_characters)

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
        elif message.startswith("rescued_"):
            character_name = message.replace("rescued_", "")
            self.rescued_characters.add(character_name)
            self.logger.info(
                f"Rescued character '{character_name}' state saved in LevelSlider."
            )

    def slide_next(self) -> None:
        next_level_num = self.current_level_num + 1
        if next_level_num > self.max_level:
            self.logger.info("Último nível concluído! Fim de jogo.")
            self.notify_observers("game_won")
            self.ended = True
            return

        # Guardar velocidades do jogador para manter o movimento
        vx, vy = self.main_character.movement.vx, self.main_character.movement.vy
        self.logger.info(f"Velocidades antes da transição: vx={vx}, vy={vy}")

        self.logger.info(f"Avançando para o nível {next_level_num}")
        self.current_level_num = next_level_num

        # Criar nova instância do nível
        self.current_level = self._create_level(self.current_level_num)

        # Posicionar o jogador na base do novo nível (margem mínima para máxima fluidez)
        self.main_character.transform.y = (
            self.window.height - self.main_character.transform.height - 2
        )

        # Manter as velocidades para continuar o movimento
        self.main_character.movement.vx = vx
        # Quando bate no topo (subindo), deve continuar subindo no próximo nível
        if vy < 0:  # estava subindo
            self.main_character.movement.vy = vy
        else:  # já estava descendo (caso raro)
            self.main_character.movement.vy = vy  # mantém a velocidade

        self.logger.info(
            f"Velocidades após a transição: vx={self.main_character.movement.vx}, vy={self.main_character.movement.vy}"
        )

        self.logger.info(
            f"Posição do jogador ajustada para y={self.main_character.transform.y}"
        )
        self._add_player_to_current_level()

    def slide_previous(self) -> None:
        prev_level_num = self.current_level_num - 1
        if prev_level_num < self.min_level:
            self.logger.info("Já está no primeiro nível, não pode retroceder.")
            return

        # Guardar velocidades do jogador para manter o movimento
        vx, vy = self.main_character.movement.vx, self.main_character.movement.vy
        self.logger.info(f"Velocidades antes da transição: vx={vx}, vy={vy}")

        self.logger.info(f"Retornando para o nível {prev_level_num}")
        self.current_level_num = prev_level_num

        # Criar nova instância do nível
        self.current_level = self._create_level(self.current_level_num)

        # Posicionar o jogador no topo do novo nível (margem mínima para máxima fluidez)
        self.main_character.transform.y = 2

        # Manter as velocidades para continuar o movimento
        self.main_character.movement.vx = vx
        # Quando bate no fundo (descendo), deve continuar descendo no nível anterior
        if vy > 0:  # estava descendo
            self.main_character.movement.vy = (
                vy * 0.9
            )  # continua descendo com 90% da velocidade (quase sem perda)
        else:  # já estava subindo (caso raro)
            self.main_character.movement.vy = vy  # mantém a velocidade

        self.logger.info(
            f"Velocidades após a transição: vx={self.main_character.movement.vx}, vy={self.main_character.movement.vy}"
        )

        self.logger.info("Posição do jogador ajustada para y=2")
        self._add_player_to_current_level()

    def update(self, delta_time: float) -> None:
        if self.ended:
            self.logger.info("O jogo já terminou, indo pra cena final.")
            return

        self.current_level.update(delta_time)
        self.altitude_hud.update(
            self.main_character, self.current_level_num, self.max_level
        )

    def draw(self) -> None:
        self.current_level.draw()
        self.altitude_hud.draw()
        self.rescued_friends_hud.draw()
