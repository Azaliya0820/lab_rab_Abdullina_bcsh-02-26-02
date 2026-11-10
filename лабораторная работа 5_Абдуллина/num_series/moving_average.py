
def check_window(window, n):
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(f"window должно быть целым ({window!r})")
    if window < 1:
        raise ValueError(f"window >= 1 ({window})")
    if window > n:
        raise ValueError(f"window ({window}) больше ряда ({n})")

def simple_moving_average(data, window):
    n = len(data)
    if n == 0:
        raise ValueError("Ряд пуст")
    check_window(window, n)
    running = sum(data[:window]); result = [running / window]
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result

def centered_moving_average(data, window):
    n = len(data)
    if n == 0:
        raise ValueError("Ряд пуст")
    check_window(window, n)
    if window % 2 == 0:
        raise ValueError("Для центрированного MA окно должно быть нечётным")
    half = window // 2
    return [sum(data[i - half:i + half + 1]) / window for i in range(half, n - half)]

def exponential_moving_average(data, alpha):
    if not data:
        raise ValueError("Ряд пуст")
    if not (0 < alpha <= 1):
        raise ValueError("0 < alpha <= 1")
    out = [float(data[0])]
    for i in range(1, len(data)):
        out.append(alpha * data[i] + (1 - alpha) * out[-1])
    return out
