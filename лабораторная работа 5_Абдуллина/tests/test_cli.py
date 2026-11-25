"""Интеграционные тесты CLI main.py через subprocess."""
import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN = PROJECT_ROOT / "main.py"


def run_cli(*args, timeout: int = 60) -> subprocess.CompletedProcess:
    """Запускает main.py отдельным процессом с cwd = корень проекта."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


class TestCliBasic:
    def test_help(self):
        res = run_cli("--help")
        assert res.returncode == 0
        assert "--kind" in res.stdout
        assert "--benchmark" in res.stdout

    def test_sine_run_ok(self):
        res = run_cli("--kind", "sine", "--n", "10",
                      "--window", "3", "--seed", "7")
        assert res.returncode == 0, res.stderr
        assert "SMA" in res.stdout
        assert "EMA" in res.stdout

    def test_invalid_n_returns_error(self):
        res = run_cli("--kind", "sine", "--n", "0")
        assert res.returncode == 1
        assert res.stderr


class TestCliSaveLoad:
    def test_save_and_load_roundtrip(self, tmp_path):
        save_path = tmp_path / "data" / "series.json"
        res = run_cli("--kind", "trend", "--n", "10",
                      "--save", str(save_path))
        assert res.returncode == 0, res.stderr
        assert save_path.exists()

        payload = json.loads(save_path.read_text(encoding="utf-8"))
        assert "data" in payload
        assert len(payload["data"]) == 10

        res = run_cli("--load", str(save_path), "--window", "3")
        assert res.returncode == 0, res.stderr
        assert "SMA" in res.stdout

    def test_load_missing_returns_error(self, tmp_path):
        res = run_cli("--load", str(tmp_path / "nope.json"))
        assert res.returncode == 1
        assert "Ошибка" in res.stderr


class TestCliExport:
    def test_export_csv(self, tmp_path):
        csv_path = tmp_path / "out.csv"
        res = run_cli("--kind", "random", "--n", "5",
                      "--export", str(csv_path))
        assert res.returncode == 0, res.stderr
        with csv_path.open(encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert rows[0] == ["i", "value"]
        assert len(rows) == 6


class TestCliJson:
    def test_json_output_parses(self):
        res = run_cli("--kind", "sine", "--n", "10",
                      "--window", "3", "--seed", "7", "--json")
        assert res.returncode == 0, res.stderr
        payload = json.loads(res.stdout)
        assert "data" in payload
        assert "sma" in payload
        assert "ema" in payload


class TestCliBenchmark:
    def test_benchmark_flag(self):
        res = run_cli("--kind", "random", "--n", "50",
                      "--window", "5", "--benchmark")
        assert res.returncode == 0, res.stderr
        assert "benchmark" in res.stdout.lower()
        assert "list" in res.stdout
        assert "deque" in res.stdout


class TestCliVariant4:
    def test_variant4_even_window(self):
        res = run_cli("--kind", "variant4", "--n", "100",
                      "--window", "4", "--seed", "42")
        assert res.returncode == 0, res.stderr
        assert "Энтропия" in res.stdout
        assert "чётное" in res.stdout

    def test_variant4_odd_window(self):
        res = run_cli("--kind", "variant4", "--n", "100",
                      "--window", "5", "--seed", "42")
        assert res.returncode == 0, res.stderr
        assert "нечётное" in res.stdout

    def test_variant4_json(self):
        res = run_cli("--kind", "variant4", "--n", "50",
                      "--window", "3", "--seed", "42", "--json")
        assert res.returncode == 0, res.stderr
        payload = json.loads(res.stdout)
        assert "variant4" in payload
        assert "entropy_bits" in payload["variant4"]
        assert "moving_median" in payload["variant4"]