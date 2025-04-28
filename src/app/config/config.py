from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Config:
    WINDOW_WIDTH: int = 1024
    WINDOW_HEIGHT: int = 768
    FPS: int = 60
    WINDOW_TITLE: str = "A Odisséia de um Prato"

    @classmethod
    def load(cls) -> "Config":
        load_dotenv()
        return cls(
            WINDOW_WIDTH=int(os.getenv("WINDOW_WIDTH", 1024)),
            WINDOW_HEIGHT=int(os.getenv("WINDOW_HEIGHT", 720)),
            FPS=int(os.getenv("FPS", 60)),
            WINDOW_TITLE=os.getenv("WINDOW_TITLE", "Pong Game"),
        )
