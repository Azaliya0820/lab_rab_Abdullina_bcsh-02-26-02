import pytest
from num_series.moving_average import (
    simple_moving_average,
    simple_moving_average_deque,
)
from num_series.deque_average import (
    simple_moving_average_deque as sma_deque_mod,
    centered_moving_average_deque,
    exponential_moving_average_deque,
)

def test_sma_deque_basic():
    assert simple_moving_average_deque([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

def test_sma_deque_matches_list():
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    for k in (1, 2, 3, 5):
        assert simple_moving_average_deque(data, k) == simple_moving_average(data, k)

def test_deque_module_matches_moving_average():
    data = [1, 2, 3, 4, 5, 6, 7]
    assert sma_deque_mod(data, 3) == simple_moving_average_deque(data, 3)

def test_centered_deque_odd_only():
    assert centered_moving_average_deque([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    with pytest.raises(ValueError):
        centered_moving_average_deque([1, 2, 3, 4], 2)

def test_ema_deque_basic():
    out = exponential_moving_average_deque([1.0, 2.0, 3.0], alpha=0.5)
    assert out[0] == 1.0
    assert out[1] == 1.5
    assert out[2] == 2.25

def test_ema_deque_invalid_alpha():
    with pytest.raises(ValueError):
        exponential_moving_average_deque([1, 2], alpha=0)
    with pytest.raises(ValueError):
        exponential_moving_average_deque([1, 2], alpha=1.5)