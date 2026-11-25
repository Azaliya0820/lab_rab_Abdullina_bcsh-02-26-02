"""Вариант 4. Целочисленный ряд N(100, 15); уникальные значения,
энтропия Шеннона, скользящая медиана (чётное/нечётное окно)."""
from __future__ import annotations

import math
import random
from bisect import bisect_left, insort
from collections import Counter
from typing import List, Optional, Sequence

# Переиспользуем median из stats.py — не дублируем код
from .stats import median  # noqa: F401  (реэкспорт)


def generate_variant4_series(
    n: int = 1000,
    seed: Optional[int] = None,
    mu: float = 100.0,
    sigma: float = 15.0,
) -> List[int]:
    """n целых чисел: round(random.gauss(mu, sigma))."""
    if n < 1:
        raise ValueError(f"n должен быть >= 1, получено: {n}")
    rng = random.Random(seed)
    return [int(round(rng.gauss(mu, sigma))) for _ in range(n)]


def count_unique(data: Sequence[int]) -> int:
    if not data:
        raise ValueError("Ряд пуст")
    return len(set(data))


def shannon_entropy(data: Sequence[int], base: float = 2.0) -> float:
    """Энтропия Шеннона по частотам: H = -Σ p_i · log_base(p_i)."""
    if not data:
        raise ValueError("Ряд пуст")
    n = len(data)
    counts = Counter(data)
    h = 0.0
    for cnt in counts.values():
        p = cnt / n
        h -= p * math.log(p, base)
    return h


def moving_median(data: Sequence[float], window: int) -> List[float]:
    """Скользящая медиана для окна любой чётности (чётное → среднее двух)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей медианы невозможен")
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > len(data):
        raise ValueError(
            f"window ({window}) больше длины ряда ({len(data)})"
        )

    buf: List[float] = []
    result: List[float] = []
    for i, x in enumerate(data):
        insort(buf, x)
        if len(buf) > window:
            old = data[i - window]
            idx = bisect_left(buf, old)
            del buf[idx]

        if i >= window - 1:
            k = len(buf)
            if k % 2 == 1:
                result.append(float(buf[k // 2]))
            else:
                result.append((buf[k // 2 - 1] + buf[k // 2]) / 2.0)
    return result


__all__ = [
    "generate_variant4_series",
    "count_unique",
    "shannon_entropy",
    "moving_median",
]