import argparse
import sys
from decimal import Decimal

from toolkit.calculator import evaluate, format_result
from toolkit.constants import DIGITS
from toolkit.converter import convert, parse_value
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Создаёт разборщик аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Консольный набор утилит: калькулятор и конвертер единиц",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    calc = commands.add_parser("calc", help="вычислить выражение")
    calc.add_argument("expression", help="арифметическое выражение в кавычках")

    convert_parser = commands.add_parser("convert", help="перевести единицы")
    convert_parser.add_argument("value", help="число для перевода")
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="исходная единица"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="целевая единица"
    )
    return parser


def is_negative_number_text(text: str) -> bool:
    """True, если строка начинается с минуса и цифры или точки."""
    return len(text) >= 2 and text[0] == "-" and (text[1] in DIGITS or text[1] == ".")


def prepare_arguments(argv: list[str]) -> list[str]:
    """Не даёт argparse принять отрицательное число за опцию."""
    if len(argv) < 2:
        return argv
    if argv[0] == "calc" and argv[1] not in ("-h", "--help") and "--" not in argv:
        return ["calc", "--", *argv[1:]]
    if argv[0] == "convert" and is_negative_number_text(argv[1]):
        return ["convert", *argv[2:], "--", argv[1]]
    return argv


def main(argv: list[str] | None = None) -> int:
    """Запускает команду и возвращает код выхода."""
    if argv is None:
        argv = sys.argv[1:]
    args = build_parser().parse_args(prepare_arguments(argv))

    try:
        if args.command == "calc":
            text = format_result(evaluate(args.expression))
        else: # convert
            value = parse_value(args.value)
            result = convert(value, args.from_unit, args.to_unit)
            text = format_result(Decimal(str(result)))

    except ToolkitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2

    print(text)
    return 0
