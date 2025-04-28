from pathlib import Path

# Root path of the project using Path for better cross-platform compatibility
ROOT_DIR = Path(__file__).parent.parent.parent.parent.resolve()
ASSETS_DIR = ROOT_DIR / "assets"


def asset_path(*paths: str) -> str:
    """
    Build full path to an asset file.

    Args:
        *paths: Variable number of path segments to join

    Returns:
        str: Absolute path to the asset

    Raises:
        FileNotFoundError: If the asset path doesn't exist
    """
    full_path = ASSETS_DIR.joinpath(*paths)
    if not full_path.exists():
        raise FileNotFoundError(f"Asset not found: {full_path}")

    return str(full_path)
