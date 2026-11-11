import pytest
from num_series.stats import mean, median, spread, summarize


def test_mean():
    assert mean([1, 2, 3]) == 2.0


def test_median_odd():
    assert median([3, 1, 2]) == 2.0


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_spread():
    assert spread([1, 5, -3, 10]) == 13.0


def test_summarize_keys_and_values():
    s = summarize([1, 2, 3, 4, 5])
    assert set(s) == {"count", "mean", "median", "spread", "min", "max"}
    assert s["count"] == 5
    assert s["mean"] == 3.0
    assert s["min"] == 1.0
    assert s["max"] == 5.0


@pytest.mark.parametrize("fn", [mean, median, spread, summarize])
def test_empty_raises(fn):
    with pytest.raises(ValueError):
        fn([])
