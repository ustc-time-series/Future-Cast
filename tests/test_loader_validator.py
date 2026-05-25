from pathlib import Path

from futurecast_bench.loader import load_series
from futurecast_bench.validator import validate_dataset


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_validate_dataset_accepts_toy_sample_data():
    result = validate_dataset("toy_energy", data_root=REPO_ROOT)

    assert result.dataset_id == "toy_energy"
    assert result.target_files == 2
    assert result.numeric_files == 2
    assert result.text_files == 2
    assert result.file_count_equal is True
    assert result.sample_alignment_ok is True
    assert result.errors == []


def test_load_series_returns_aligned_rows_with_context():
    series = load_series("toy_energy", series_id="toy_turbine_001", data_root=REPO_ROOT, limit=2)

    assert series.dataset_id == "toy_energy"
    assert series.series_id == "toy_turbine_001"
    assert len(series.rows) == 2
    assert series.rows[0]["timestamp"] == "2024-01-01 00:00:00"
    assert series.rows[0]["target_power"] == "10.0"
    assert series.rows[0]["wind_speed"] == "5.2"
    assert "Toy wind turbine" in series.rows[0]["text_exogenous"]
