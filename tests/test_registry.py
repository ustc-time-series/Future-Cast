from futurecast_bench.registry import get_dataset, list_datasets


def test_registry_contains_toy_sample_dataset():
    datasets = list_datasets()

    assert "toy_energy" in [dataset.dataset_id for dataset in datasets]


def test_get_dataset_returns_core_metadata():
    dataset = get_dataset("toy_energy")

    assert dataset.dataset_id == "toy_energy"
    assert dataset.domain == "sample"
    assert dataset.frequency == "1H"
    assert dataset.target_column == "target_power"
    assert dataset.available_in_repo is True
# Repository maintenance refresh: 2026-08-05.
