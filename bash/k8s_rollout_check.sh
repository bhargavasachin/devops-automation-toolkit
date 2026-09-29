#!/usr/bin/env bash
set -euo pipefail

namespace="${1:?namespace is required}"
deployment="${2:?deployment is required}"
timeout="${3:-5m}"

kubectl -n "$namespace" rollout status "deployment/$deployment" --timeout="$timeout"
