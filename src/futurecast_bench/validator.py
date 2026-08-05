"""Validation utilities for FutureCast-Bench lightweight datasets."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

from .loader import KEY_COLUMNS
from .registry import resolve_dataset_path


@dataclass(frozen=True)
class ValidationResult:
    """Summary of a lightweight FutureCast dataset validation pass."""

    dataset_id: str
    dataset_path: str
    target_files: int
    numeric_files: int
    text_files: int
    file_count_equal: bool
    sampled_series: int
    sample_alignment_ok: bool
    errors: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _csv_files(root: Path) -> list[Path]:
    return sorted(root.glob("**/*.csv"))


def _pick_samples(files: list[Path], sample_size: int) -> list[Path]:
    if len(files) <= sample_size:
        return files
    if sample_size <= 1:
        return [files[0]]
    indexes = sorted({0, len(files) // 2, len(files) - 1})
    return [files[index] for index in indexes[:sample_size]]


def _paired_file(dataset_path: Path, kind: str, target_file: Path) -> Path | None:
    target_root = dataset_path / "processed" / "target"
    other_root = dataset_path / "processed" / kind
    candidate = other_root / target_file.relative_to(target_root)
    if candidate.exists():
        return candidate
    matches = [path for path in _csv_files(other_root) if path.stem == target_file.stem]
    return matches[0] if matches else None


def _read_keys(path: Path) -> list[tuple[str, str]]:
    keys: list[tuple[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [key for key in KEY_COLUMNS if key not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} is missing key columns: {missing}")
        for row in reader:
            keys.append((row["timestamp"], row["series_id"]))
    return keys


def validate_dataset(
    dataset_id: str,
    data_root: str | Path | None = None,
    sample_size: int = 3,
) -> ValidationResult:
    """Validate folder structure and sampled target/numeric/text alignment."""

    errors: list[str] = []
    dataset_path = resolve_dataset_path(dataset_id, data_root)
    target_root = dataset_path / "processed" / "target"
    numeric_root = dataset_path / "processed" / "numeric_exogenous"
    text_root = dataset_path / "processed" / "text_exogenous"

    for root in [target_root, numeric_root, text_root]:
        if not root.exists():
            errors.append(f"Missing required directory: {root}")

    target_files = _csv_files(target_root) if target_root.exists() else []
    numeric_files = _csv_files(numeric_root) if numeric_root.exists() else []
    text_files = _csv_files(text_root) if text_root.exists() else []
    file_count_equal = len(target_files) == len(numeric_files) == len(text_files)
    if not file_count_equal:
        errors.append(
            "Target, numeric exogenous, and text exogenous CSV counts differ: "
            f"{len(target_files)}, {len(numeric_files)}, {len(text_files)}"
        )

    sampled = _pick_samples(target_files, sample_size)
    sample_alignment_ok = True
    for target_file in sampled:
        numeric_file = _paired_file(dataset_path, "numeric_exogenous", target_file)
        text_file = _paired_file(dataset_path, "text_exogenous", target_file)
        if numeric_file is None or text_file is None:
            sample_alignment_ok = False
            errors.append(f"Missing paired numeric/text file for {target_file}")
            continue
        try:
            target_keys = _read_keys(target_file)
            numeric_keys = _read_keys(numeric_file)
            text_keys = _read_keys(text_file)
        except ValueError as exc:
            sample_alignment_ok = False
            errors.append(str(exc))
            continue
        if not (target_keys == numeric_keys == text_keys):
            sample_alignment_ok = False
            errors.append(f"Sample alignment mismatch for {target_file}")

    return ValidationResult(
        dataset_id=dataset_id,
        dataset_path=str(dataset_path),
        target_files=len(target_files),
        numeric_files=len(numeric_files),
        text_files=len(text_files),
        file_count_equal=file_count_equal,
        sampled_series=len(sampled),
        sample_alignment_ok=sample_alignment_ok,
        errors=errors,
    )
# Repository maintenance refresh: 2026-08-05.
