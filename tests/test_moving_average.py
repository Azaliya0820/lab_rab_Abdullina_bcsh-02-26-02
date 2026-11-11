import pytest
from num_series.moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)


def test_sma_length():
    assert len(simple_moving_average([1, 2, 3, 4, 5], 3)) == 3


def test_sma_values():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_sma_window_1():
    assert simple_moving_average([1.0, 2.0, 3.0], 1) == [1.0, 2.0, 3.0]


def test_sma_window_too_large():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2, 3], 5)


def test_sma_invalid_window():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2, 3], 0)


def test_sma_empty():
    with pytest.raises(ValueError):
        simple_moving_average([], 1)


def test_centered_ma_odd():
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_centered_ma_even_raises():
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3, 4, 5], 2)


def test_ema_basic():
    assert exponential_moving_average([1, 2, 3], 0.5) == [1.0, 1.5, 2.25]


def test_ema_single():
    assert exponential_moving_average([5.0], 0.5) == [5.0]


@pytest.mark.parametrize("alpha", [0, -0.1, 1.5])
def test_ema_alpha_invalid(alpha):
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], alpha)
