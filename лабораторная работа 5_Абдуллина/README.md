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
    ├── pytest.ini
    ├── run_self_tests.py
    ├── main.py
    └── README.md

## Запуск
    python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7

## Примеры
    # Сохранить ряд в JSON
    python main.py --kind random --n 50 --save data/random.json
    # Прочитать ряд из файла
    python main.py --load data/random.json --window 5
    # Пайплайн: генерация → сохранение → чтение → анализ
    python main.py --kind sine --n 30 --save data/s.json
    python main.py --load data/s.json --window 3
    # Экспорт в CSV
    python main.py --kind trend --n 30 --export out.csv
    # Вывод в JSON
    python main.py --kind sine --n 20 --json

## Тесты
    pytest -q
    python run_self_tests.py
## Лабораторная 5.1 — расширение
### Модуль `deque_average.py`
Реализация SMA / центрированного MA / EMA через `collections.deque`.
Сравнение с «индексной» версией в `moving_average.py`.

### Замер производительности SMA
```bash
python main.py --kind random --n 5000 --window 20 --benchmark
