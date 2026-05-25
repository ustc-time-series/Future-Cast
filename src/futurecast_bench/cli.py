"""Command-line interface for FutureCast-Bench."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from .loader import load_series
from .registry import get_dataset, list_datasets, spec_to_dict
from .validator import validate_dataset


def _add_data_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Repository root or processed dataset root. Defaults to the installed checkout root.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="futurecast", description="FutureCast-Bench utility CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List registered datasets")

    inspect_parser = subparsers.add_parser("inspect", help="Show registry metadata for one dataset")
    inspect_parser.add_argument("dataset_id")

    validate_parser = subparsers.add_parser("validate", help="Validate a processed dataset layout")
    validate_parser.add_argument("dataset_id")
    validate_parser.add_argument("--sample-size", type=int, default=3)
    _add_data_root(validate_parser)

    sample_parser = subparsers.add_parser("sample", help="Print aligned rows from one series")
    sample_parser.add_argument("dataset_id")
    sample_parser.add_argument("--series-id", default=None)
    sample_parser.add_argument("--limit", type=int, default=5)
    _add_data_root(sample_parser)

    return parser


def _print_dataset_list() -> None:
    print("dataset_id\tdomain\tfrequency\tseries_count\tlocation")
    for spec in list_datasets():
        location = "in-repo sample" if spec.available_in_repo else "external data"
        series_count = "" if spec.series_count is None else str(spec.series_count)
        print(f"{spec.dataset_id}\t{spec.domain}\t{spec.frequency}\t{series_count}\t{location}")


def _print_validation(result) -> None:
    for key, value in result.to_dict().items():
        if isinstance(value, bool):
            value = str(value).lower()
        print(f"{key}: {value}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            _print_dataset_list()
            return 0
        if args.command == "inspect":
            print(json.dumps(spec_to_dict(get_dataset(args.dataset_id)), indent=2, ensure_ascii=False))
            return 0
        if args.command == "validate":
            result = validate_dataset(args.dataset_id, data_root=args.data_root, sample_size=args.sample_size)
            _print_validation(result)
            return 0 if not result.errors else 1
        if args.command == "sample":
            series = load_series(
                args.dataset_id,
                series_id=args.series_id,
                data_root=args.data_root,
                limit=args.limit,
            )
            print(json.dumps(asdict(series), indent=2, ensure_ascii=False))
            return 0
    except Exception as exc:
        print(f"futurecast: error: {exc}")
        return 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
