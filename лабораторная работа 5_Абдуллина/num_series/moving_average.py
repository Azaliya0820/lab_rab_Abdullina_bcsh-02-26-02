import time
from collections import deque
from typing import List, Sequence

def check_window(window: int, n: int) -> None:
    """Окно — целое ≥ 1 и не больше длины ряда."""
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(
            f"window должно быть целым числом (получено: {window!r})"
        )
    if window < 1:
        raise ValueError(
            f"window должно быть >= 1 (получено: {window})"
        )
    if window > n:
        raise ValueError(
            f"окно ({window}) больше ряда ({n})"
        )

def simple_moving_average(data: Sequence[float],
                          window: int) -> List[float]:
    """SMA через бегущую сумму (O(n))."""
    n = len(data)
    if n == 0:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, n)

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result

#Самостоятельное задание
def centered_moving_average(data: Sequence[float],
                            window: int) -> List[float]:
    """Центрированное MA: окно должно быть нечётным, выход по центру."""
    n = len(data)
    if n == 0:
        raise ValueError("Ряд пуст: расчёт CMA невозможен")
    check_window(window, n)
    if window % 2 == 0:
        raise ValueError(
            f"Для центрированного MA окно должно быть нечётным "
            f"(получено: {window})"
        )
    half = window // 2
    return [
        sum(data[i - half : i + half + 1]) / window
        for i in range(half, n - half)
    ]

def exponential_moving_average(data: Sequence[float],
                               alpha: float) -> List[float]:
    """EMA[0]=data[0]; EMA[i]=alpha*data[i]+(1-alpha)*EMA[i-1], 0<alpha<=1."""
    if not data:
        raise ValueError("Ряд пуст: расчёт EMA невозможен")
    if not (0 < alpha <= 1):
        raise ValueError(
            f"alpha должно быть в диапазоне (0, 1] (получено: {alpha})"
        )
    result = [float(data[0])]
    for i in range(1, len(data)):
        result.append(alpha * data[i] + (1 - alpha) * result[-1])
    return result

# ---------- ЛР 5.1: SMA через deque + бенчмарк ----------

def simple_moving_average_deque(data: Sequence[float],
                                window: int) -> List[float]:
    """SMA через deque(maxlen=window). O(n) по времени, O(window) по памяти."""
    n = len(data)
    if n == 0:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, n)

    buf: deque = deque(maxlen=window)
    running = 0.0
    result: List[float] = []
    for i, x in enumerate(data):
        if len(buf) == window:
            running -= buf[0]
        buf.append(x)
        running += x
        if i >= window - 1:
            result.append(running / window)
    return result

def benchmark_moving_average(data: Sequence[float],
                             window: int,
                             repeats: int = 1000) -> dict:
    """Замеряет среднее время выполнения SMA для list и deque (в секундах)."""
    check_window(window, len(data))

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}