from pathlib import Path

import yaml

from futurecast_bench.validator import validate_dataset
from scripts.prepare_toy_energy import prepare_toy_energy


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_prepare_toy_energy_writes_futurecast_layout(tmp_path: Path):
    source = REPO_ROOT / "examples" / "raw" / "toy_energy" / "toy_energy_raw.csv"
    output = tmp_path / "toy_energy"

    prepare_toy_energy(source_csv=source, output_dir=output)

    target = output / "processed" / "target" / "toy_turbine_001.csv"
    numeric = output / "processed" / "numeric_exogenous" / "toy_turbine_001.csv"
    text = output / "processed" / "text_exogenous" / "toy_turbine_001.csv"
    task = output / "tasks" / "toy_energy_power.yaml"

    assert target.exists()
    assert numeric.exists()
    assert text.exists()
    assert task.exists()

    with task.open(encoding="utf-8") as fh:
        task_data = yaml.safe_load(fh)
    assert task_data["dataset_id"] == "toy_energy"
    assert task_data["target"]["column"] == "target_power"

    result = validate_dataset("toy_energy", data_root=tmp_path)
    assert result.file_count_equal is True
    assert result.sample_alignment_ok is True
    assert result.errors == []

    direct_result = validate_dataset("toy_energy", data_root=output)
    assert direct_result.file_count_equal is True
    assert direct_result.sample_alignment_ok is True
    assert direct_result.errors == []
