"""Пакет алгоритмической обработки числовых рядов.

Публичный API:
    Генерация: random_series, sine_series, trend_series
    Статистика: mean, median, spread, summarize
    Скользящие средние: simple_moving_average, centered_moving_average,
                        exponential_moving_average,
                        simple_moving_average_deque, benchmark_moving_average
    Deque-версии: simple_moving_average_deque (из deque_average),
                  centered_moving_average_deque,
                  exponential_moving_average_deque
    Ввод-вывод: save_series_json, load_series_json,
                load_series_txt, load_series_csv, load_series_auto
    Вариант 4: generate_variant4_series, count_unique,
               shannon_entropy, moving_median
"""
from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
    simple_moving_average_deque,
    benchmark_moving_average,
)
from .deque_average import (
    simple_moving_average_deque as simple_moving_average_deque_v2,
    centered_moving_average_deque,
    exponential_moving_average_deque,
)
from .variant4 import (
    generate_variant4_series,
    count_unique,
    shannon_entropy,
    moving_median,
)
from .io_json import save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto

__all__ = [
    # генерация
    "random_series", "sine_series", "trend_series",
    # статистика
    "mean", "median", "spread", "summarize",
    # скользящие средние (list)
    "simple_moving_average", "centered_moving_average",
    "exponential_moving_average",
    # ЛР 5.1: SMA через deque + бенчмарк
    "simple_moving_average_deque",
    "benchmark_moving_average",
    # ЛР 5.1: отдельный модуль deque_average
    "simple_moving_average_deque_v2",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    # Вариант 4
    "generate_variant4_series",
    "count_unique",
    "shannon_entropy",
    "moving_median",
    # ввод-вывод
    "save_series_json", "load_series_json",
    "load_series_txt", "load_series_csv", "load_series_auto",
]
__version__ = "1.2.0"