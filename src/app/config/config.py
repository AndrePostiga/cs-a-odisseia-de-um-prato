from dataclasses import dataclass
from dotenv import load_dotenv
import os
import pathlib


@dataclass
class Config:
    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080
    FPS: int = 60
    WINDOW_TITLE: str = "A Odisséia de um Prato"

    @classmethod
    def load(cls) -> "Config":
        project_root = pathlib.Path(__file__).parent.parent.parent.parent
        dotenv_path = project_root / ".env"

        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            print(f"Loaded .env from: {dotenv_path}")
        else:
            print(f"Warning: .env file not found at {dotenv_path}")
            load_dotenv()

        return cls(
            WINDOW_WIDTH=int(os.getenv("WINDOW_WIDTH", 1920)),
            WINDOW_HEIGHT=int(os.getenv("WINDOW_HEIGHT", 1080)),
            FPS=int(os.getenv("FPS", 60)),
            WINDOW_TITLE=os.getenv("WINDOW_TITLE", "A Odisséia de um Prato"),
        )
