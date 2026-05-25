from pathlib import Path

from futurecast_bench.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_cli_list_prints_toy_dataset(capsys):
    code = main(["list"])

    output = capsys.readouterr().out
    assert code == 0
    assert "toy_energy" in output
    assert "sample" in output


def test_cli_validate_prints_alignment_status(capsys):
    code = main(["validate", "toy_energy", "--data-root", str(REPO_ROOT)])

    output = capsys.readouterr().out
    assert code == 0
    assert "sample_alignment_ok: true" in output
    assert "target_files: 2" in output


def test_cli_sample_prints_context_rows(capsys):
    code = main(["sample", "toy_energy", "--series-id", "toy_turbine_001", "--limit", "1", "--data-root", str(REPO_ROOT)])

    output = capsys.readouterr().out
    assert code == 0
    assert "toy_turbine_001" in output
    assert "target_power" in output
    assert "text_exogenous" in output
