from decimal import Decimal, DecimalException, InvalidOperation

from toolkit.constants import (
    BINARY_OPERATORS,
    DIGITS,
    OPERATOR_CHARS,
    PRECEDENCE,
    ROUNDING_STEP,
)
from toolkit.errors import (
    CalculationError,
    DivisionByZeroError,
    ExpressionError,
    InputError,
)

type Tokens = list[tuple[str, Decimal | str]]

def should_pop(top: str, new: str) -> bool:
    """True, если оператор с вершины стека нужно вытолкнуть перед новым"""
    if new == "**": # правоассоц.
        return PRECEDENCE[top] > PRECEDENCE[new]
    return PRECEDENCE[top] >= PRECEDENCE[new]


def is_unary_position(tokens: Tokens) -> bool:
    """True, если следующий + или - будет унарным."""
    if not tokens:
        return True

    kind, value = tokens[-1]
    return kind == "OP" and value != ")"


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


def validate(tokens: Tokens) -> None:
    """Проверка порядка токенов и скобок"""
    if not tokens:
        raise ExpressionError("Пустое выражение")

    expect_operand = True
    depth = 0
    previous = ""
    for kind, value in tokens:
        symbol = str(value)
        if expect_operand:
            if kind == "NUM":
                expect_operand = False

            elif symbol == "(":
                depth += 1

            elif symbol == ")":
                if previous == "(":
                    raise ExpressionError("Пустые скобки")
                raise ExpressionError("Пропущен операнд")

            elif symbol in BINARY_OPERATORS:
                if previous in BINARY_OPERATORS:
                    raise ExpressionError("Два оператора подряд")
                raise ExpressionError("Пропущен операнд")

        elif kind == "NUM" or symbol == "(":
            raise ExpressionError("Пропущен оператор")

        elif symbol == ")":
            depth -= 1
            if depth < 0:
                raise ExpressionError("Несбалансированные скобки")

        else:
            expect_operand = True

        previous = symbol
    if expect_operand:
        raise ExpressionError("Пропущен операнд")

    if depth != 0:
        raise ExpressionError("Несбалансированные скобки")


def _euclid_divmod(a: Decimal, b: Decimal) -> tuple[Decimal, Decimal]:
    """Евклидово деление: a = q*b + r, 0 <= r < |b|, q целое."""
    if b == 0:
        raise DivisionByZeroError("Деление на ноль")

    q, r = divmod(a, b)
    if r < 0:
        r += abs(b)
        q += -1 if b > 0 else 1
    return q, r


def quotient(a: Decimal, b: Decimal) -> Decimal:
    """Неполное частное."""
    return _euclid_divmod(a, b)[0]


def remainder(a: Decimal, b: Decimal) -> Decimal:
    """Остаток от деления."""
    return _euclid_divmod(a, b)[1]


def apply_operator(symbol: str, left: Decimal, right: Decimal) -> Decimal:
    """Применяет бинарный оператор к двум числам"""
    match symbol:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            if right == 0:
                raise DivisionByZeroError("Деление на ноль")
            return left / right
        case "//":
            return quotient(left, right)
        case "%":
            return remainder(left, right)
        case _: # **
            if left == 0 and right < 0:
                raise DivisionByZeroError("Деление на ноль")
            return left**right


def to_rpn(tokens: Tokens) -> Tokens:
    """Перевод токены в обратную польскую запис"""
    output: Tokens = []
    stack: list[str] = []

    for kind, value in tokens:
        if kind == "NUM":
            output.append((kind, value))
            continue

        symbol = str(value)

        if symbol in ("u+", "u-") or symbol == "(":
            stack.append(symbol)

        elif symbol == ")":
            while stack[-1] != "(":
                output.append(("OP", stack.pop()))
            stack.pop()

        else:
            while (
                stack
                and stack[-1] != "("
                and should_pop(stack[-1], symbol)
            ):
                output.append(("OP", stack.pop()))

            stack.append(symbol)

    while stack:
        output.append(("OP", stack.pop()))
    return output


def evaluate_rpn(rpn: Tokens) -> Decimal:
    """Вычисляет выражение в обратной польской записи."""
    stack = []
    for kind, value in rpn:
        if kind == "NUM":
            stack.append(Decimal(value))
            continue

        symbol = str(value)

        if symbol == "u+":
            stack.append(+stack.pop())
        elif symbol == "u-":
            stack.append(-stack.pop())

        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(apply_operator(symbol, left, right))
    return Decimal(stack.pop())


def calculate(tokens: Tokens) -> Decimal:
    """Переводит токены в RPN и вычисляет результат."""
    return evaluate_rpn(to_rpn(tokens))


def evaluate(expression: str) -> Decimal:
    """Вычисляет выражение."""
    tokens = tokenize(expression)
    validate(tokens)

    try:
        return calculate(tokens)
    except DecimalException:
        raise CalculationError("Ошибка вычисления")


def format_result(value: Decimal) -> str:
    """Округляет результат до 4 знаков и превращает в строку."""
    rounded = value.quantize(ROUNDING_STEP)
    text = format(rounded, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text
