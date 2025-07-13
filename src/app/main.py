from app.config.log_config import setup_logging
from app.config.config import Config
from app.pplay.window import Window
from app.core.game import Game
import logging


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    config = Config.load()
    logger.info(f"Configuration loaded: {config}")

    window = Window(
        width=config.WINDOW_WIDTH,
        height=config.WINDOW_HEIGHT,
    )
    window.set_title(config.WINDOW_TITLE)

    game = Game(window)
    game.run()


if __name__ == "__main__":
    main()
