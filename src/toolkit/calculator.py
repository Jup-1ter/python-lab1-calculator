from decimal import Decimal, InvalidOperation

from toolkit.constants import DIGITS, OPERATOR_CHARS
from toolkit.errors import InputError

type Tokens = list[tuple[str, Decimal | str]]

def is_unary_position(tokens: Tokens) -> bool:
    """True, если следующий + или - будет унарным."""
    if not tokens:
        return True

    kind, value = tokens[-1]
    return kind == "OP"


def tokenize(expr: str) -> Tokens:
    """Разбивка выражения на токены."""
    tokens: Tokens = []
    i = 0

    while i < len(expr):
        char = expr[i]
        if char.isspace():
            i += 1

        elif char in DIGITS or char == ".":
            start = i
            while i < len(expr) and (expr[i] in DIGITS or expr[i] == "."):
                i += 1
            text = expr[start:i]
            try:
                number = Decimal(text)
            except InvalidOperation:
                raise InputError(f"Неверное числовое значение: {text}")
            tokens.append(("NUM", number))

        elif char in OPERATOR_CHARS:
            symbol = char
            step = 1

            if char in "*/" and i + 1 < len(expr) and expr[i + 1] == char:
                symbol = char + char
                step = 2
            elif char in "+-" and is_unary_position(tokens):
                symbol = "u" + char
            tokens.append(("OP", symbol))
            i += step

        else:
            raise InputError(f"Недопустимый символ: {char}")
    return tokens
