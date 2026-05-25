#!/usr/bin/env python3
"""Process the toy raw energy CSV into the FutureCast lightweight layout."""

from __future__ import annotations

import argparse
import csv
import shutil
from collections import defaultdict
from pathlib import Path

import yaml


DATASET_ID = "toy_energy"
DOMAIN = "sample"
FREQUENCY = "1H"
TARGET_COLUMN = "target_power"
NUMERIC_COLUMNS = ["wind_speed", "temperature", "hour"]
TEXT_COLUMN = "text_exogenous"
KEY_COLUMNS = ["timestamp", "series_id"]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _task_yaml(series_count: int) -> dict[str, object]:
    return {
        "dataset_id": DATASET_ID,
        "domain": DOMAIN,
        "frequency": FREQUENCY,
        "series_granularity": "one toy wind turbine per series_id",
        "series_count": series_count,
        "target": {
            "file_pattern": "processed/target/{series_id}.csv",
            "column": TARGET_COLUMN,
        },
        "numeric_exogenous": {
            "file_pattern": "processed/numeric_exogenous/{series_id}.csv",
            "columns": NUMERIC_COLUMNS,
        },
        "text_exogenous": {
            "file_pattern": "processed/text_exogenous/{series_id}.csv",
            "column": TEXT_COLUMN,
        },
        "alignment_rule": {
            "key_columns": KEY_COLUMNS,
            "require_equal_length": True,
        },
        "forecasting_windows": {
            "short": {
                "context_length": 3,
                "prediction_length": 1,
                "context_description": "past 3 hours",
                "prediction_description": "next 1 hour",
            }
        },
    }


def prepare_toy_energy(source_csv: Path, output_dir: Path) -> None:
    """Convert a single raw toy CSV into target/numeric/text/task files."""

    if output_dir.exists():
        shutil.rmtree(output_dir)

    required = [*KEY_COLUMNS, TARGET_COLUMN, *NUMERIC_COLUMNS, TEXT_COLUMN]
    by_series: dict[str, list[dict[str, str]]] = defaultdict(list)
    with source_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [column for column in required if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{source_csv} is missing required columns: {missing}")
        for row in reader:
            by_series[row["series_id"]].append(row)

    if not by_series:
        raise ValueError(f"{source_csv} contains no rows.")

    for series_id, rows in sorted(by_series.items()):
        rows = sorted(rows, key=lambda row: row["timestamp"])
        target_rows = [{**{key: row[key] for key in KEY_COLUMNS}, TARGET_COLUMN: row[TARGET_COLUMN]} for row in rows]
        numeric_rows = [{**{key: row[key] for key in KEY_COLUMNS}, **{key: row[key] for key in NUMERIC_COLUMNS}} for row in rows]
        text_rows = [{**{key: row[key] for key in KEY_COLUMNS}, TEXT_COLUMN: row[TEXT_COLUMN]} for row in rows]

        _write_csv(output_dir / "processed" / "target" / f"{series_id}.csv", [*KEY_COLUMNS, TARGET_COLUMN], target_rows)
        _write_csv(
            output_dir / "processed" / "numeric_exogenous" / f"{series_id}.csv",
            [*KEY_COLUMNS, *NUMERIC_COLUMNS],
            numeric_rows,
        )
        _write_csv(
            output_dir / "processed" / "text_exogenous" / f"{series_id}.csv",
            [*KEY_COLUMNS, TEXT_COLUMN],
            text_rows,
        )

    tasks_dir = output_dir / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    with (tasks_dir / "toy_energy_power.yaml").open("w", encoding="utf-8") as fh:
        yaml.safe_dump(_task_yaml(series_count=len(by_series)), fh, sort_keys=False, allow_unicode=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("examples/raw/toy_energy/toy_energy_raw.csv"))
    parser.add_argument("--output", type=Path, default=Path("examples/sample_data/toy_energy"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepare_toy_energy(source_csv=args.source, output_dir=args.output)
    print(f"Wrote FutureCast toy dataset to {args.output}")


if __name__ == "__main__":
    main()
