import pytest

from toolkit.converter import convert, parse_value
from toolkit.errors import InputError, RangeError, UnitError


@pytest.mark.parametrize(
    "value, from_unit, to_unit, expected",
    [
        (1, "km", "m", 1000),
        (100, "cm", "m", 1),
        (1500, "g", "kg", 1.5),
        (1, "KM", "M", 1000),
        (0, "c", "k", 273.15),
        (32, "f", "c", 0),
        (-40, "c", "f", -40),
    ],
)
def test_convert_returns_expected_value(
    value: float, from_unit: str, to_unit: str, expected: float
) -> None:
    """Перевод даёт ожидаемое значение."""
    assert convert(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value, from_unit, to_unit, expected",
    [
        (-273.15, "c", "k", 0),
        (-459.67, "f", "k", 0),
        (0, "k", "c", -273.15),
    ],
)
def test_convert_absolute_zero_boundary_is_allowed(
    value: float, from_unit: str, to_unit: str, expected: float
) -> None:
    """Температура ровно в абсолютном нуле допустима."""
    assert convert(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("5.", 5),
        (".5", 0.5),
        ("-5.", -5),
        ("+3", 3),
    ],
)
def test_parse_value_returns_expected_number(text: str, expected: float) -> None:
    """Корректные строки превращаются в числа."""
    assert parse_value(text) == pytest.approx(expected)


@pytest.mark.parametrize(
    "text",
    ["1e3", "nan", "inf", "", ".", "-", "1.2.3", "abc"],
)
def test_parse_value_invalid_text_raises_error(text: str) -> None:
    """Неверная запись числа даёт ошибку."""
    with pytest.raises(InputError):
        parse_value(text)


def test_parse_value_too_large_number_raises_error() -> None:
    """Число, не помещающееся в float, даёт ошибку."""
    with pytest.raises(RangeError):
        parse_value("9" * 400)


@pytest.mark.parametrize(
    "from_unit, to_unit",
    [("xx", "m"), ("m", "xx"), ("m", "")],
)
def test_convert_unknown_unit_raises_error(from_unit: str, to_unit: str) -> None:
    """Неизвестная единица даёт ошибку."""
    with pytest.raises(UnitError):
        convert(1, from_unit, to_unit)


@pytest.mark.parametrize(
    "from_unit, to_unit",
    [("m", "kg"), ("kg", "c"), ("f", "mm")],
)
def test_convert_incompatible_units_raises_error(from_unit: str, to_unit: str) -> None:
    """Единицы из разных групп несовместимы."""
    with pytest.raises(UnitError):
        convert(1, from_unit, to_unit)


@pytest.mark.parametrize(
    "value, from_unit, to_unit",
    [(-1, "m", "km"), (-1, "g", "kg"), (-0.001, "mm", "m")],
)
def test_convert_negative_length_or_mass_raises_error(
    value: float, from_unit: str, to_unit: str
) -> None:
    """Отрицательные длина и масса запрещены."""
    with pytest.raises(RangeError):
        convert(value, from_unit, to_unit)


@pytest.mark.parametrize(
    "value, from_unit",
    [(-300, "c"), (-460, "f"), (-1, "k")],
)
def test_convert_below_absolute_zero_raises_error(value: float, from_unit: str) -> None:
    """Температура ниже абсолютного нуля запрещена."""
    with pytest.raises(RangeError):
        convert(value, from_unit, "k")


def test_convert_infinite_result_raises_error() -> None:
    """Слишком большой результат даёт ошибку."""
    with pytest.raises(RangeError):
        convert(1e308, "km", "mm")
