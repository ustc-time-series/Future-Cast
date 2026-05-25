"""Dataset registry for FutureCast-Bench."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class DatasetSpec:
    """Static metadata needed to locate and inspect a FutureCast dataset."""

    dataset_id: str
    domain: str
    frequency: str
    path: str
    forecasting_unit: str
    target_column: str
    numeric_exogenous: tuple[str, ...]
    text_column: str = "text_exogenous"
    series_count: int | None = None
    available_in_repo: bool = False
    description: str = ""
    note: str = ""


def repo_root() -> Path:
    """Return the repository root for editable installs and local checkouts."""

    return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def _registry() -> dict[str, DatasetSpec]:
    with resources.files("futurecast_bench.configs").joinpath("datasets.yaml").open(
        "r", encoding="utf-8"
    ) as fh:
        raw = yaml.safe_load(fh)

    specs: dict[str, DatasetSpec] = {}
    for item in raw["datasets"]:
        spec = DatasetSpec(
            dataset_id=item["dataset_id"],
            domain=item["domain"],
            frequency=str(item["frequency"]),
            path=item["path"],
            forecasting_unit=item["forecasting_unit"],
            target_column=item["target_column"],
            numeric_exogenous=tuple(item.get("numeric_exogenous", [])),
            text_column=item.get("text_column", "text_exogenous"),
            series_count=item.get("series_count"),
            available_in_repo=bool(item.get("available_in_repo", False)),
            description=item.get("description", ""),
            note=item.get("note", ""),
        )
        specs[spec.dataset_id] = spec
    return specs


def list_datasets() -> list[DatasetSpec]:
    """List registered datasets sorted by dataset id."""

    return sorted(_registry().values(), key=lambda spec: spec.dataset_id)


def get_dataset(dataset_id: str) -> DatasetSpec:
    """Return metadata for a registered dataset."""

    try:
        return _registry()[dataset_id]
    except KeyError as exc:
        known = ", ".join(spec.dataset_id for spec in list_datasets())
        raise KeyError(f"Unknown dataset_id '{dataset_id}'. Known datasets: {known}") from exc


def spec_to_dict(spec: DatasetSpec) -> dict[str, Any]:
    """Convert a dataset spec to a JSON/YAML-friendly dictionary."""

    return {
        "dataset_id": spec.dataset_id,
        "domain": spec.domain,
        "frequency": spec.frequency,
        "path": spec.path,
        "forecasting_unit": spec.forecasting_unit,
        "target_column": spec.target_column,
        "numeric_exogenous": list(spec.numeric_exogenous),
        "text_column": spec.text_column,
        "series_count": spec.series_count,
        "available_in_repo": spec.available_in_repo,
        "description": spec.description,
        "note": spec.note,
    }


def resolve_dataset_path(dataset_id: str, data_root: str | Path | None = None) -> Path:
    """Resolve a dataset path from registry metadata and an optional data root."""

    spec = get_dataset(dataset_id)
    roots = [Path(data_root).expanduser()] if data_root is not None else [repo_root()]
    candidates: list[Path] = []
    for root in roots:
        if (root / "processed").exists():
            candidates.append(root)
        candidates.extend(
            [
                root / spec.path,
                root / spec.domain / spec.dataset_id,
                root / spec.dataset_id,
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    formatted = "\n".join(f"- {candidate}" for candidate in candidates)
    raise FileNotFoundError(
        f"Could not locate dataset '{dataset_id}'. Tried:\n{formatted}\n"
        "Pass --data-root pointing to the repository root or processed dataset root."
    )
