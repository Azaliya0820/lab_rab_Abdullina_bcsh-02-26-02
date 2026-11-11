"""Запуск проверок без pytest."""
import sys
import tempfile
import traceback
from pathlib import Path

TESTS = []


def case(fn):
    TESTS.append(fn)
    return fn


@case
def test_sma():
    from num_series import simple_moving_average
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


@case
def test_ema():
    from num_series import exponential_moving_average
    assert exponential_moving_average([1, 2, 3], 0.5) == [1.0, 1.5, 2.25]


@case
def test_stats():
    from num_series import mean, median, spread
    assert mean([1, 2, 3]) == 2.0
    assert median([3, 1, 2]) == 2.0
    assert spread([1, 5]) == 4.0


@case
def test_json_roundtrip():
    from num_series import save_series_json, load_series_json
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "s.json"
        data = [1.0, 2.5, -3.0]
        save_series_json(data, p)
        assert load_series_json(p) == data


@case
def test_errors():
    from num_series import simple_moving_average
    try:
        simple_moving_average([], 3)
    except ValueError:
        pass
    else:
        raise AssertionError("ожидалось ValueError на пустом ряде")


def main_run() -> int:
    failures = 0
    for fn in TESTS:
        try:
            fn()
            print(f"[OK]   {fn.__name__}")
        except Exception:
            failures += 1
            print(f"[FAIL] {fn.__name__}")
            traceback.print_exc()
    total = len(TESTS)
    print(f"\nИтого: {total - failures}/{total} успешно")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main_run())
