# toolkit

Консольный набор утилит: калькулятор арифметических выражений и конвертер единиц измерения.

## Установка

```bash
uv sync
source .venv/bin/activate
```

## Запуск

```bash
uv run python -m toolkit calc "10/4 + 2"
uv run python -m toolkit convert 36.6 --from c --to f
```

Справка: `python -m toolkit --help`, `python -m toolkit calc --help`.
