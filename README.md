# DevOps Automation Toolkit

Small, focused utilities for cloud and Kubernetes operations. The goal is to automate repetitive checks without hiding the underlying commands or making an operator depend on a large framework.

> **Portfolio note:** These are public reference utilities based on automation patterns used in engineering work. They do not contain employer-specific credentials, endpoints or proprietary logic.

## Principles

- Fail clearly when required input is missing.
- Prefer read-only inspection by default.
- Keep shell commands visible and composable.
- Return useful exit codes so tools work in CI as well as from a terminal.
- Make destructive operations explicit rather than implicit.

## Tools

| Tool | Purpose |
|---|---|
| `python/json_merge.py` | Merge JSON configuration layers with predictable precedence |
| `python/validate_config.py` | Validate a JSON configuration file against required keys |
| `python/k8s_diagnose.py` | Collect a compact first-pass Kubernetes diagnosis |
| `bash/terraform_changed.sh` | Identify whether a change set contains Terraform files |
| `bash/k8s_rollout_check.sh` | Wait for a deployment rollout and return a useful exit code |

All examples operate on user-supplied files or the local `kubectl` context. No credentials are embedded.

## Examples

```bash
# Merge a base config with environment overrides
python3 python/json_merge.py examples/environment.json overrides.json

# Validate required keys before a deployment reads the file
python3 python/validate_config.py examples/environment.json

# Diagnose a workload (exit code is non-zero if any kubectl call fails)
python3 python/k8s_diagnose.py platform-demo platform-app
```
