# num_series_app — алгоритмическая обработка числовых рядов

Лабораторная работа №5. Модульное консольное приложение на Python:
генерация рядов, базовая статистика, скользящие средние
(SMA, центрированное MA, EMA), экспорт/импорт JSON и CSV.

## Структура

    num_series_app/
    ├── num_series/
    │   ├── __init__.py
    │   ├── generator.py
    │   ├── stats.py
    │   ├── moving_average.py
    │   ├── io_json.py
    │   └── io_file.py
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_generator.py
    │   ├── test_stats.py
    │   ├── test_moving_average.py
    │   └── test_cli.py
    ├── pytest.ini
    ├── run_self_tests.py
    ├── main.py
    └── README.md

## Запуск

    python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7

## Примеры

    python main.py --kind random --n 50 --save data/random.json
    python main.py --load data/random.json --window 5
    python main.py --kind sine --n 30 --save data/s.json
    python main.py --load data/s.json --window 3
    python main.py --kind trend --n 30 --export out.csv
    python main.py --kind sine --n 20 --json

## Тесты

    pytest -q
    python run_self_tests.py
