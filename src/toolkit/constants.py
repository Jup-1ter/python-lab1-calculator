from decimal import Decimal

DIGITS = "0123456789"
OPERATOR_CHARS = "+-*/%()"
BINARY_OPERATORS = {"+", "-", "*", "/", "//", "%", "**"}

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
    "u+": 3,
    "u-": 3,
    "**": 4,
}

# Округление результата: 4 знака после точки
ROUNDING_STEP = Decimal("0.0001")
EXPONENT_FORMAT = ".4e"
EXPONENT_THRESHOLD = Decimal("1e15")

LENGTH_TO_METERS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
MASS_TO_KILOGRAMS = {"g": 0.001, "kg": 1.0}

# Кельвины = (значение + сдвиг) * масштаб
TEMPERATURE_OFFSETS = {"c": 273.15, "f": 459.67, "k": 0.0}
TEMPERATURE_SCALES = {"c": 1.0, "f": 5 / 9, "k": 1.0}
