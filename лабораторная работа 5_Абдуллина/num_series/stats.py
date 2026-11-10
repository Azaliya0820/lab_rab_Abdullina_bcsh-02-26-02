
def _ensure_not_empty(data):
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")

def mean(data):
    _ensure_not_empty(data)
    return sum(data) / len(data)

def median(data):
    _ensure_not_empty(data)
    s = sorted(data); k = len(s) // 2
    return float(s[k]) if len(s) % 2 else (s[k - 1] + s[k]) / 2.0

def spread(data):
    _ensure_not_empty(data)
    return float(max(data) - min(data))

def summarize(data):
    _ensure_not_empty(data)
    return {"count": len(data), "mean": mean(data), "median": median(data),
            "spread": spread(data), "min": float(min(data)), "max": float(max(data))}
