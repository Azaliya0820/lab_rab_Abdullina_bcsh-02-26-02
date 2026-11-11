import json
from main import main


def test_cli_generation_ok(capsys):
    rc = main(["--kind", "sine", "--n", "10", "--window", "3", "--seed", "7"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "SMA" in out
    assert "EMA" in out


def test_cli_invalid_n(capsys):
    rc = main(["--kind", "sine", "--n", "0"])
    assert rc == 1


def test_cli_load_missing(capsys):
    rc = main(["--load", "nonexistent_file.json"])
    assert rc == 1


def test_cli_save_and_load_roundtrip(tmp_path, capsys):
    save_path = tmp_path / "data" / "series.json"
    rc = main(["--kind", "trend", "--n", "10", "--save", str(save_path)])
    assert rc == 0
    assert save_path.exists()

    with save_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    assert "data" in payload
    assert len(payload["data"]) == 10

    rc = main(["--load", str(save_path), "--window", "3"])
    assert rc == 0


def test_cli_export_csv(tmp_path, capsys):
    csv_path = tmp_path / "out.csv"
    rc = main(["--kind", "random", "--n", "5", "--export", str(csv_path)])
    assert rc == 0
    lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "i,value"
    assert len(lines) == 6
