#!/usr/bin/env python3
"""Merge JSON configuration files from left to right."""

import json
import sys
from pathlib import Path


def merge(left, right):
    if isinstance(left, dict) and isinstance(right, dict):
        result = dict(left)
        for key, value in right.items():
            result[key] = merge(result[key], value) if key in result else value
        return result
    return right


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: json_merge.py base.json override.json [override.json ...]")

    merged = {}
    for name in sys.argv[1:]:
        path = Path(name)
        with path.open(encoding="utf-8") as handle:
            merged = merge(merged, json.load(handle))

    json.dump(merged, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
