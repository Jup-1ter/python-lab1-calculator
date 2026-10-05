class ToolkitError(Exception):
    """Базовая ошибка пользователя: неверный ввод или невозможное вычисление."""


class InputError(ToolkitError):
    """Недопустимый символ или неверная запись числа."""


class ExpressionError(ToolkitError):
    """Неправильная структура выражения: порядок токенов, скобки."""


class CalculationError(ToolkitError):
    """Выражение невычислимо."""


class DivisionByZeroError(CalculationError):
    """Деление на ноль."""


class UnitError(ToolkitError):
    """Неизвестная или несовместимая единица."""


class RangeError(ToolkitError):
    """Значение вне допустимого диапазона."""
