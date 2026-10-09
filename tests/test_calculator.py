from decimal import Decimal

import pytest

from toolkit.calculator import evaluate, tokenize
from toolkit.errors import CalculationError, ExpressionError, InputError


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2+2", "4"),
        ("10/4 + 2", "4.5"),
        ("7 + 8 / 4 - 1", "8"),
        ("-5 + 2 * -3", "-11"),
        ("2 + 3.5 * -4", "-12"),
        ("(2+3)*4", "20"),
        ("((1 + 2) * (3 + 4))", "21"),
        (".5 + 5.", "5.5"),
        ("0.1 + 0.2", "0.3"),
        ("  2   +   2  ", "4"),
        ("--5", "5"),
        ("+-5", "-5"),
        ("-(2+3)", "-5"),
        ("2 ** -1", "0.5"),
        ("-2 ** 2", "-4"),
        ("7 // 3", "2"),
        ("7 % 3", "1"),
        ("7.5 // 2", "3"),
    ],
)
def test_evaluate_returns_expected_value(expression: str, expected: str) -> None:
    """Выражение вычисляется в ожидаемое значение."""
    assert evaluate(expression) == Decimal(expected)


def test_evaluate_does_not_round_to_four_digits() -> None:
    """Результат evaluate округляется только контекстом Decimal."""
    assert evaluate("1/3") == Decimal("0.3333333333333333333333333333")


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


@pytest.mark.parametrize("expression", ["", "   ", "\t\n"])
def test_evaluate_empty_expression_raises_error(expression: str) -> None:
    """Пустое выражение и пробелы дают ошибку."""
    with pytest.raises(ExpressionError):
        evaluate(expression)


@pytest.mark.parametrize("expression", ["2 $ 3", "1e3", "1.2.3", "."])
def test_evaluate_invalid_token_raises_error(expression: str) -> None:
    """Недопустимый символ или неверное число дают ошибку."""
    with pytest.raises(InputError):
        evaluate(expression)


@pytest.mark.parametrize(
    "expression",
    ["2 +", "2 * * 3", "2 3", "2 (3)", "()", "(2 + )", "* 3"],
)
def test_evaluate_wrong_token_order_raises_error(expression: str) -> None:
    """Пропущенный операнд или оператор дают ошибку."""
    with pytest.raises(ExpressionError):
        evaluate(expression)


@pytest.mark.parametrize("expression", ["(2 + 3", "2 + 3)", "((1 + 2)"])
def test_evaluate_unbalanced_parentheses_raises_error(expression: str) -> None:
    """Несбалансированные скобки дают ошибку."""
    with pytest.raises(ExpressionError):
        evaluate(expression)


@pytest.mark.parametrize("expression", ["(-8) ** 0.5", "10 ** 1000000", "0 ** 0"])
def test_evaluate_decimal_error_raises_error(expression: str) -> None:
    """Ошибки Decimal превращаются в ToolkitError."""
    with pytest.raises(CalculationError):
        evaluate(expression)
