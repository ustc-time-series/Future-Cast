"""Lightweight CSV loader for FutureCast-Bench datasets."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .registry import get_dataset, resolve_dataset_path


KEY_COLUMNS = ("timestamp", "series_id")


@dataclass(frozen=True)
class SeriesData:
    """Aligned rows for one FutureCast forecasting series."""

    dataset_id: str
    series_id: str
    rows: list[dict[str, str]]


def _csv_files(root: Path) -> list[Path]:
    return sorted(root.glob("**/*.csv"))


def _read_csv(path: Path, limit: int | None = None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
            if limit is not None and len(rows) >= limit:
                break
    return rows


def _target_file(dataset_path: Path, series_id: str | None) -> Path:
    files = _csv_files(dataset_path / "processed" / "target")
    if not files:
        raise FileNotFoundError(f"No target CSV files found under {dataset_path}")
    if series_id is None:
        return files[0]
    for path in files:
        if path.stem == series_id:
            return path
    raise FileNotFoundError(f"Series '{series_id}' was not found in {dataset_path}")


def _paired_file(dataset_path: Path, kind: str, target_file: Path) -> Path:
    target_root = dataset_path / "processed" / "target"
    other_root = dataset_path / "processed" / kind
    relative = target_file.relative_to(target_root)
    candidate = other_root / relative
    if candidate.exists():
        return candidate

    matches = [path for path in _csv_files(other_root) if path.stem == target_file.stem]
    if matches:
        return matches[0]
    raise FileNotFoundError(f"Could not find {kind} file matching {target_file.name}")


def _assert_aligned(target: list[dict[str, str]], numeric: list[dict[str, str]], text: list[dict[str, str]]) -> None:
    if not (len(target) == len(numeric) == len(text)):
        raise ValueError("Target, numeric exogenous, and text exogenous row counts differ.")
    for index, (target_row, numeric_row, text_row) in enumerate(zip(target, numeric, text)):
        for key in KEY_COLUMNS:
            if target_row.get(key) != numeric_row.get(key) or target_row.get(key) != text_row.get(key):
                raise ValueError(f"Alignment mismatch at row {index} for key '{key}'.")


def load_series(
    dataset_id: str,
    series_id: str | None = None,
    data_root: str | Path | None = None,
    limit: int | None = None,
) -> SeriesData:
    """Load one aligned target/numeric/text series as dictionaries.

    This is intentionally lightweight and CSV-native. It is meant for quick inspection,
    smoke tests, and small examples; large-scale training code can build on the same
    alignment contract with streaming or framework-specific loaders.
    """

    get_dataset(dataset_id)
    dataset_path = resolve_dataset_path(dataset_id, data_root)
    target_path = _target_file(dataset_path, series_id)
    numeric_path = _paired_file(dataset_path, "numeric_exogenous", target_path)
    text_path = _paired_file(dataset_path, "text_exogenous", target_path)

    target_rows = _read_csv(target_path, limit)
    numeric_rows = _read_csv(numeric_path, limit)
    text_rows = _read_csv(text_path, limit)
    _assert_aligned(target_rows, numeric_rows, text_rows)

    merged_rows: list[dict[str, str]] = []
    for target_row, numeric_row, text_row in zip(target_rows, numeric_rows, text_rows):
        merged = dict(target_row)
        for row in [numeric_row, text_row]:
            for key, value in row.items():
                if key not in KEY_COLUMNS:
                    merged[key] = value
        merged_rows.append(merged)

    loaded_series_id = merged_rows[0]["series_id"] if merged_rows else target_path.stem
    return SeriesData(dataset_id=dataset_id, series_id=loaded_series_id, rows=merged_rows)
# Repository maintenance refresh: 2026-08-05.
