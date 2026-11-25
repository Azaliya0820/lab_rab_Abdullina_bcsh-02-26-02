"""Автономный запуск проверок без pytest.

Использование:
    python run_self_tests.py
Возвращает 0 при успехе, 1 при первом провале.
"""
import sys
import tempfile
import traceback
from pathlib import Path

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def _approx_eq(a, b, eps=1e-9):
    """Приближённое сравнение двух float или двух списков float."""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(abs(x - y) < eps for x, y in zip(a, b))
    return abs(a - b) < eps


# ---------- генератор ----------
@check
def check_generator_basics():
    from num_series import random_series, sine_series, trend_series
    assert len(random_series(10, seed=1)) == 10
    assert random_series(20, seed=42) == random_series(20, seed=42)
    assert len(sine_series(15, seed=0)) == 15
    assert trend_series(3, step=2.0, noise=0.0) == [0.0, 2.0, 4.0]


@check
def check_generator_rejects_bad_n():
    from num_series.generator import _validate_n
    for bad in (0, -1, 3.5, "abc", None):
        try:
            _validate_n(bad)
        except ValueError:
            continue
        raise AssertionError(f"_validate_n({bad!r}) не бросил ValueError")


# ---------- статистика ----------
@check
def check_stats():
    from num_series import mean, median, spread, summarize
    assert mean([1, 2, 3]) == 2.0
    assert median([3, 1, 2]) == 2.0
    assert median([1, 2, 3, 4]) == 2.5
    assert spread([-10, 10]) == 20.0
    s = summarize([1, 2, 3, 4, 5])
    assert s["count"] == 5 and s["mean"] == 3.0


@check
def check_stats_empty():
    from num_series import mean, median, spread, summarize
    for fn in (mean, median, spread, summarize):
        try:
            fn([])
        except ValueError:
            continue
        raise AssertionError(f"{fn.__name__}([]) не бросил ValueError")


# ---------- скользящие средние ----------
@check
def check_sma():
    from num_series import simple_moving_average
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    assert simple_moving_average([1.0, 2.5, -3.0, 4.0], 1) == [1.0, 2.5, -3.0, 4.0]


@check
def check_sma_matches_naive():
    """Быстрая SMA ≈ наивная SMA с точностью 1e-9."""
    import random
    from num_series import simple_moving_average
    rng = random.Random(0)
    data = [rng.uniform(-10, 10) for _ in range(50)]
    w = 7
    naive = [sum(data[i:i + w]) / w for i in range(len(data) - w + 1)]
    fast = simple_moving_average(data, w)
    assert _approx_eq(fast, naive), (
        f"fast != naive\nmax diff = "
        f"{max(abs(a - b) for a, b in zip(fast, naive))}"
    )


@check
def check_cma():
    from num_series import centered_moving_average
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    try:
        centered_moving_average([1, 2, 3, 4], 2)
    except ValueError:
        pass
    else:
        raise AssertionError("CMA не отвергнул чётное окно")


@check
def check_ema():
    from num_series import exponential_moving_average
    assert exponential_moving_average([1, 2, 3], 0.5) == [1.0, 1.5, 2.25]
    for bad_alpha in (0, -0.1, 1.5):
        try:
            exponential_moving_average([1, 2, 3], bad_alpha)
        except ValueError:
            continue
        raise AssertionError(f"EMA не отвергнул alpha={bad_alpha}")


# ---------- deque ----------
@check
def check_deque_equivalence():
    """list-версия ≈ deque-версия с точностью 1e-9 (разный порядок операций!)."""
    import random
    from num_series import (
        simple_moving_average, simple_moving_average_deque,
        centered_moving_average, centered_moving_average_deque,
        exponential_moving_average, exponential_moving_average_deque,
    )
    rng = random.Random(42)
    data = [rng.uniform(-100, 100) for _ in range(200)]

    for w in (1, 3, 7, 25):
        a = simple_moving_average(data, w)
        b = simple_moving_average_deque(data, w)
        assert _approx_eq(a, b), f"SMA mismatch for w={w}"

        a = centered_moving_average(data, w)
        b = centered_moving_average_deque(data, w)
        assert _approx_eq(a, b), f"CMA mismatch for w={w}"

    for alpha in (0.1, 0.5, 1.0):
        a = exponential_moving_average(data, alpha)
        b = exponential_moving_average_deque(data, alpha)
        assert _approx_eq(a, b), f"EMA mismatch for alpha={alpha}"


@check
def check_benchmark_structure():
    from num_series import benchmark_moving_average
    data = list(range(100))
    res = benchmark_moving_average(data, window=5, repeats=10)
    assert set(res) == {"list", "deque"}
    assert res["list"] >= 0 and res["deque"] >= 0


# ---------- I/O ----------
@check
def check_json_roundtrip():
    from num_series import save_series_json, load_series_json
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "s.json"
        data = [1.0, 2.5, -3.0]
        save_series_json(data, p, meta={"kind": "test"})
        loaded, meta = load_series_json(p, with_meta=True)
        assert loaded == data
        assert meta["kind"] == "test"


@check
def check_txt_parse():
    from num_series import load_series_txt
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "d.txt"
        p.write_text("# comment\n1.5\n\n2.0\n3.0\n", encoding="utf-8")
        assert load_series_txt(p) == [1.5, 2.0, 3.0]


@check
def check_csv_parse():
    from num_series import load_series_csv
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "d.csv"
        p.write_text("v1,v2\n1.0;2.0\n3.0,4.0\n", encoding="utf-8")
        assert load_series_csv(p) == [1.0, 2.0, 3.0, 4.0]


# ---------- variant4 ----------
@check
def check_variant4_basics():
    from num_series import (
        generate_variant4_series, count_unique,
        shannon_entropy, moving_median,
    )
    arr = generate_variant4_series(n=500, seed=42)
    assert len(arr) == 500
    assert all(isinstance(x, int) for x in arr)
    assert count_unique(arr) > 1
    assert shannon_entropy(arr) > 0
    assert moving_median([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    assert moving_median([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]


# ---------- runner ----------
def main_run() -> int:
    failures = 0
    total = len(CHECKS)
    for fn in CHECKS:
        try:
            fn()
            print(f"[OK]   {fn.__name__}")
        except Exception:
            failures += 1
            print(f"[FAIL] {fn.__name__}")
            traceback.print_exc()
    print(f"\nИтого: {total - failures}/{total} успешно")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main_run())