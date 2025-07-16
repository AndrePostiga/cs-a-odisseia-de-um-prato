from app.config.log_config import setup_logging
from app.config.config import Config
from app.pplay.window import Window
from app.core.game import Game
from app.seedwork.path_helper import asset_path
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
    try:
        icon_path = asset_path("images", "hud", "potato_icon.png")
        window.set_icon(icon_path)
    except FileNotFoundError as e:
        logger.warning(f"Could not set window icon: {e}")

    game = Game(window)
    game.run()


if __name__ == "__main__":
    main()
