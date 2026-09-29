#!/usr/bin/env python3
"""Validate a small environment configuration before it reaches a pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {
    "name": str,
    "region": str,
    "environment": str,
}


def validate(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return [f"file not found: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]

    if not isinstance(data, dict):
        return ["top-level JSON value must be an object"]

    errors: list[str] = []
    for key, expected_type in REQUIRED.items():
        value = data.get(key)
        if value is None:
            errors.append(f"missing required field: {key}")
        elif not isinstance(value, expected_type):
            errors.append(f"{key} must be a {expected_type.__name__}")
        elif isinstance(value, str) and not value.strip():
            errors.append(f"{key} must not be empty")

    environment = data.get("environment")
    if isinstance(environment, str) and environment not in {"dev", "staging", "prod"}:
        errors.append("environment must be one of: dev, staging, prod")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deployment configuration")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    errors = validate(args.file)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.file} passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
