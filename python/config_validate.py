#!/usr/bin/env python3
"""Validate a small deployment configuration before it reaches a pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED = ("name", "environment", "region")


def validate(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return [f"file not found: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    errors = []
    if not isinstance(data, dict):
        return ["top-level value must be an object"]

    for key in REQUIRED:
        if not data.get(key):
            errors.append(f"missing required field: {key}")

    environment = data.get("environment")
    if environment and environment not in {"dev", "staging", "prod"}:
        errors.append(f"unsupported environment: {environment}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <config.json>", file=sys.stderr)
        return 2

    errors = validate(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("configuration is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
