import os
import subprocess
import sys
from pathlib import Path


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Запускает toolkit в отдельном процессе."""
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *arguments],
        cwd=Path(__file__).parent.parent / "src",
        capture_output=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )


def test_cli_calc_prints_result() -> None:
    """Команда calc печатает результат выражения."""
    result = run_cli("calc", "2 + 3")
    assert result.returncode == 0
    assert result.stdout.strip() == "5"


def test_cli_calc_negative_expression_works_without_separator() -> None:
    """Выражение с минусом в начале работает без --."""
    result = run_cli("calc", "-5+2")
    assert result.returncode == 0
    assert result.stdout.strip() == "-3"


def test_cli_calc_division_by_zero_returns_error() -> None:
    """Ошибка вычисления даёт код 2 и сообщение в stderr."""
    result = run_cli("calc", "1 / 0")
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith("Ошибка:")


def test_cli_calc_without_expression_returns_argparse_error() -> None:
    """Команда calc без выражения завершается ошибкой argparse."""
    result = run_cli("calc")
    assert result.returncode == 2
    assert result.stdout == ""


def test_cli_convert_prints_result() -> None:
    """Команда convert печатает результат перевода."""
    result = run_cli("convert", "100", "--from", "cm", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "1"


def test_cli_convert_negative_value_and_uppercase_units() -> None:
    """Отрицательное значение и заглавные единицы работают."""
    result = run_cli("convert", "-40", "--from", "C", "--to", "F")
    assert result.returncode == 0
    assert result.stdout.strip() == "-40"


def test_cli_convert_negative_value_with_trailing_dot() -> None:
    """Значение вида -5. переносится в конец и разбирается."""
    result = run_cli("convert", "-5.", "--from", "c", "--to", "f")
    assert result.returncode == 0
    assert result.stdout.strip() == "23"


def test_cli_convert_incompatible_units_returns_error() -> None:
    """Несовместимые единицы дают код 2 и сообщение в stderr."""
    result = run_cli("convert", "1", "--from", "m", "--to", "kg")
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith("Ошибка:")


def test_cli_help_returns_zero() -> None:
    """Опция --help завершается с кодом 0."""
    result = run_cli("--help")
    assert result.returncode == 0
