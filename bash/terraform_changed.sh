#!/usr/bin/env bash
set -euo pipefail

base_ref="${1:-HEAD~1}"
head_ref="${2:-HEAD}"

if git diff --name-only "$base_ref" "$head_ref" | grep -Eq '(^|/)(.*\.tf|.*\.tfvars)$'; then
  echo "Terraform-related changes detected"
  exit 0
fi

echo "No Terraform-related changes detected"
exit 1
