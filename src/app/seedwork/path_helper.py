import sys
from pathlib import Path


def get_assets_dir() -> Path:
    """
    Retorna o caminho para a pasta de assets, funcionando tanto em modo de
    desenvolvimento quanto empacotado com PyInstaller.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Rodando em um bundle PyInstaller
        # Os assets são colocados na pasta 'assets' dentro do diretório temporário
        return Path(sys._MEIPASS) / "assets"
    else:
        # Rodando em modo de desenvolvimento
        # O ROOT_DIR é a raiz do projeto
        ROOT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
        return ROOT_DIR / "assets"


def asset_path(*paths: str) -> str:
    """
    Monta o caminho absoluto para um asset.

    Args:
        *paths: Segmentos do caminho para juntar.

    Returns:
        str: Caminho absoluto para o asset.

    Raises:
        FileNotFoundError: Se o caminho do asset não existir.
    """
    assets_dir = get_assets_dir()
    full_path = assets_dir.joinpath(*paths)
    if not full_path.exists():
        raise FileNotFoundError(f"Asset not found: {full_path}")

    return str(full_path)
