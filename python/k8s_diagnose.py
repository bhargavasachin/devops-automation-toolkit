#!/usr/bin/env python3
"""Print a compact first-pass Kubernetes workload diagnosis."""

import argparse
import subprocess
import sys


def run(args):
    result = subprocess.run(args, check=False, text=True, capture_output=True)
    print(f"$ {' '.join(args)}")
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("namespace")
    parser.add_argument("deployment")
    args = parser.parse_args()

    commands = [
        ["kubectl", "-n", args.namespace, "get", "deployment", args.deployment],
        ["kubectl", "-n", args.namespace, "get", "pods", "-l", f"app={args.deployment}"],
        ["kubectl", "-n", args.namespace, "get", "events", "--sort-by=.lastTimestamp"],
    ]

    failed = 0
    for command in commands:
        if run(command) != 0:
            failed += 1

    if failed:
        print(f"{failed} kubectl command(s) failed.", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
