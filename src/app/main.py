from app.config.log_config import setup_logging
from app.ioc_container import Container


def main() -> None:
    # Setup logging first thing
    setup_logging()

    container = Container()
    game = container.game()
    game.run()


if __name__ == "__main__":
    main()
