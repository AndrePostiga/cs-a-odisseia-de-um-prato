from dependency_injector import containers, providers
from app.config.config import Config
from app.pplay.window import Window
from app.core.game import Game


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config.load)

    @staticmethod
    def create_window(config: Config) -> Window:
        window = Window(
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
        )
        window.set_title(config.WINDOW_TITLE)
        return window

    window = providers.Singleton(create_window, config=config)

    game = providers.Singleton(
        Game,
        window=window,
    )
