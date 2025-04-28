import os
import sys
import logging
import logging.config
from types import TracebackType
from typing import Type, Dict, Any


def setup_logging(
    *, default_level: str = "INFO", service_name: str = "cs_a_odisseia_de_um_prato"
) -> None:
    # (e.g. DEBUG in dev, INFO in prod)
    level = os.getenv("LOG_LEVEL", default_level).upper()

    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            # root logger
            "": {
                "level": level,
                "handlers": ["console"],
            },
            # silence verbose libraries if needed
            "pygame": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.LoggerAdapter(logging.getLogger(), {"service": service_name})
    logging.config.dictConfig(config)

    def handle_exception(
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception
