from decimal import Decimal

from toolkit.calculator import tokenize


def test_tokenize_marks_unary_operators() -> None:
    """Унарные знаки получают символы u+ и u-, бинарные остаются прежними."""
    assert tokenize("2 - -3") == [
        ("NUM", Decimal(2)),
        ("OP", "-"),
        ("OP", "u-"),
        ("NUM", Decimal(3)),
    ]


def test_tokenize_joins_double_operators() -> None:
    """Пары ** и // собираются в один токен."""
    assert tokenize("2 ** 3 // 1") == [
        ("NUM", Decimal(2)),
        ("OP", "**"),
        ("NUM", Decimal(3)),
        ("OP", "//"),
        ("NUM", Decimal(1)),
    ]
