import pytest
from num_series.generator import (
    random_series, sine_series, trend_series, _validate_n,
)


def test_random_series_length():
    assert len(random_series(10)) == 10


def test_random_series_in_range():
    data = random_series(100, low=-5, high=5, seed=1)
    assert all(-5 <= v <= 5 for v in data)


def test_random_series_seed_reproducible():
    assert random_series(10, seed=42) == random_series(10, seed=42)


def test_random_series_different_seeds():
    assert random_series(10, seed=1) != random_series(10, seed=2)


def test_random_series_invalid_bounds():
    with pytest.raises(ValueError):
        random_series(5, low=10, high=0)


@pytest.mark.parametrize("n", [0, -1, -100])
def test_invalid_n(n):
    with pytest.raises(ValueError):
        _validate_n(n)


def test_sine_series_length():
    assert len(sine_series(20)) == 20


def test_sine_series_no_noise_is_deterministic():
    a = sine_series(10, amplitude=1, frequency=1, noise=0)
    b = sine_series(10, amplitude=1, frequency=1, noise=0)
    assert a == b


def test_trend_series_basic():
    data = trend_series(5, start=0, step=2, noise=0)
    assert data == [0, 2, 4, 6, 8]
