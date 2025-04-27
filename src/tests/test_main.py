from app.main import main
from pytest import CaptureFixture
from typing import Any


def test_main(
    capsys: CaptureFixture[Any],
) -> None:
    main()
    captured = capsys.readouterr()
    assert "Hello world!" in captured.out
