"""Тесты модуля num_series.io_file (TXT, CSV и автовыбор формата)."""
import pytest

from num_series.io_file import (
    load_series_txt,
    load_series_csv,
    load_series_auto,
)
from num_series.io_json import save_series_json


class TestLoadSeriesTxt:
    def test_valid_txt_with_comments_and_blanks(self, tmp_path):
        p = tmp_path / "data.txt"
        p.write_text("# комментарий\n\n1.5\n\n2\n3.25\n\n", encoding="utf-8")
        assert load_series_txt(p) == [1.5, 2.0, 3.25]

    def test_non_numeric_line_reports_lineno(self, tmp_path):
        p = tmp_path / "bad.txt"
        p.write_text("1.0\n2.0\nabc\n", encoding="utf-8")
        with pytest.raises(ValueError, match=":3:"):
            load_series_txt(p)

    def test_empty_file_raises(self, tmp_path):
        p = tmp_path / "empty.txt"
        p.write_text("# только комментарий\n\n", encoding="utf-8")
        with pytest.raises(ValueError, match="не содержит чисел"):
            load_series_txt(p)

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(ValueError, match="не найден"):
            load_series_txt(tmp_path / "nope.txt")


class TestLoadSeriesCsv:
    def test_csv_with_header_and_mixed_separators(self, tmp_path):
        p = tmp_path / "data.csv"
        p.write_text(
            "value1,value2\n1.0, 2.5\n3.0; 4.5\n", encoding="utf-8"
        )
        assert load_series_csv(p) == [1.0, 2.5, 3.0, 4.5]

    def test_csv_without_header(self, tmp_path):
        p = tmp_path / "plain.csv"
        p.write_text("1,2,3\n4,5,6\n", encoding="utf-8")
        assert load_series_csv(p) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    def test_bad_row_after_header_raises(self, tmp_path):
        p = tmp_path / "bad.csv"
        p.write_text("value\n1.0\nabc\n", encoding="utf-8")
        with pytest.raises(ValueError, match=":3:"):
            load_series_csv(p)

    def test_empty_file_raises(self, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_text("# nothing\n", encoding="utf-8")
        with pytest.raises(ValueError, match="не содержит чисел"):
            load_series_csv(p)


class TestLoadSeriesAuto:
    def test_auto_json(self, tmp_path):
        p = tmp_path / "data.json"
        save_series_json([1.0, 2.0, 3.0], p)
        assert load_series_auto(p) == [1.0, 2.0, 3.0]

    def test_auto_txt(self, tmp_path):
        p = tmp_path / "data.txt"
        p.write_text("1.0\n2.0\n3.0\n", encoding="utf-8")
        assert load_series_auto(p) == [1.0, 2.0, 3.0]

    def test_auto_csv(self, tmp_path):
        p = tmp_path / "data.csv"
        p.write_text("1,2,3\n", encoding="utf-8")
        assert load_series_auto(p) == [1.0, 2.0, 3.0]

    def test_auto_unknown_extension_falls_back(self, tmp_path):
        p = tmp_path / "data.unknown"
        p.write_text("1.0\n2.0\n", encoding="utf-8")
        assert load_series_auto(p) == [1.0, 2.0]