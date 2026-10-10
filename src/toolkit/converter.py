import math

from toolkit.constants import (
    DIGITS,
    LENGTH_TO_METERS,
    MASS_TO_KILOGRAMS,
    TEMPERATURE_OFFSETS,
    TEMPERATURE_SCALES,
)
from toolkit.errors import InputError, RangeError, UnitError


def is_number_text(text: str) -> bool:
    """True, если строка является корректной записью числа"""
    body = text
    if text[:1] in ("+", "-"):
        body = text[1:]

    dots = 0
    digits = 0

    for char in body:
        if char == ".":
            dots += 1
        elif char in DIGITS:
            digits += 1
        else:
            return False
    return dots <= 1 and digits > 0


def parse_value(text: str) -> float:
    """Разбирает строку VALUE в число."""
    if not is_number_text(text):
        raise InputError(f"Неверное числовое значение: {text}")

    value = float(text)
    if math.isinf(value):
        raise RangeError("Слишком большое число")

    return value


def get_group(unit: str) -> str:
    """Возвращает группу единицы."""
    if unit in LENGTH_TO_METERS:
        return "l"
    if unit in MASS_TO_KILOGRAMS:
        return "m"
    if unit in TEMPERATURE_OFFSETS:
        return "t"
    raise UnitError(f"Неизвестная единица: {unit}")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Переводит температуру через кельвины."""
    if value < -TEMPERATURE_OFFSETS[from_unit]:
        raise RangeError("Температура ниже абсолютного нуля")

    kelvin = (value + TEMPERATURE_OFFSETS[from_unit]) * TEMPERATURE_SCALES[from_unit]
    return kelvin / TEMPERATURE_SCALES[to_unit] - TEMPERATURE_OFFSETS[to_unit]


def convert_with_table(
    value: float, from_unit: str, to_unit: str, table: dict[str, float]
) -> float:
    """Переводит длину или массу через базовую единицу."""
    if value < 0:
        raise RangeError("Длина и масса не могут быть отрицательными")
    return value * table[from_unit] / table[to_unit]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Переводит значение из одной единицы в другую."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    from_group = get_group(from_unit)
    to_group = get_group(to_unit)
    
    if from_group != to_group:
        raise UnitError(f"Несовместимые единицы: {from_unit} и {to_unit}")
    match from_group:
        case "l":
            result = convert_with_table(value, from_unit, to_unit, LENGTH_TO_METERS)
        case "m":
            result = convert_with_table(value, from_unit, to_unit, MASS_TO_KILOGRAMS)
        case _: # t
            result = convert_temperature(value, from_unit, to_unit)

    if math.isinf(result):
        raise RangeError("Слишком большое число")
    return result
