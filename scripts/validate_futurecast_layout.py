#!/usr/bin/env python3
"""Validate a FutureCast lightweight processed dataset layout."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from futurecast_bench.validator import validate_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_id", help="Registered dataset id, for example toy_energy")
    parser.add_argument("--data-root", type=Path, default=Path("."))
    parser.add_argument("--sample-size", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = validate_dataset(args.dataset_id, data_root=args.data_root, sample_size=args.sample_size)
    print(yaml.safe_dump(result.to_dict(), sort_keys=False, allow_unicode=True))
    if result.errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
