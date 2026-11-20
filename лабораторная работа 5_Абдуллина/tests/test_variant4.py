import pytest
from num_series.variant4 import (
    generate_variant4_series,
    count_unique,
    shannon_entropy,
    median,
    moving_median,
)

def test_generate_length_and_type():
    arr = generate_variant4_series(n=1000, seed=42)
    assert len(arr) == 1000
    assert all(isinstance(x, int) for x in arr)

def test_generate_reproducible():
    assert (generate_variant4_series(100, seed=7)
            == generate_variant4_series(100, seed=7))

def test_count_unique():
    assert count_unique([1, 1, 2, 2, 3]) == 3
    assert count_unique([5, 5, 5]) == 1

def test_entropy_basics():
    assert shannon_entropy([5, 5, 5, 5]) == pytest.approx(0.0)
    assert shannon_entropy([1, 2, 3, 4]) == pytest.approx(2.0)
    assert shannon_entropy([1, 1, 2, 2]) == pytest.approx(1.0)

def test_median_odd_even():
    assert median([1, 2, 3]) == 2.0
    assert median([1, 2, 3, 4]) == 2.5

def test_moving_median_odd():
    assert moving_median([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

def test_moving_median_even():
    assert moving_median([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]
    assert moving_median([1, 1, 1, 2, 2, 2], 4) == [1.0, 1.5, 2.0]

def test_moving_median_repeated():
    assert moving_median([5] * 10, 3) == [5.0] * 8
    assert moving_median([5] * 10, 4) == [5.0] * 7

def test_moving_median_k_1_and_n():
    d = [3, 1, 4, 1, 5]
    assert moving_median(d, 1) == [float(x) for x in d]
    assert moving_median(d, len(d)) == [median(d)]

def test_moving_median_matches_naive():
    arr = generate_variant4_series(n=200, seed=42)
    for k in (2, 3, 4, 5, 10, 11):
        got = moving_median(arr, k)
        naive = [median(arr[i:i + k]) for i in range(len(arr) - k + 1)]
        assert got == naive, f"Mismatch k={k}"

def test_moving_median_invalid():
    with pytest.raises(ValueError):
        moving_median([], 3)
    with pytest.raises(ValueError):
        moving_median([1, 2, 3], 0)
    with pytest.raises(ValueError):
        moving_median([1, 2, 3], 4)