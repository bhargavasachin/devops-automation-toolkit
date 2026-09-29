import json

from python.validate_config import validate


def write_config(tmp_path, value):
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    return path


def test_valid_config(tmp_path):
    path = write_config(
        tmp_path,
        {"name": "platform", "region": "us-ashburn-1", "environment": "prod"},
    )
    assert validate(path) == []


def test_missing_required_field(tmp_path):
    path = write_config(tmp_path, {"name": "platform", "region": "us-ashburn-1"})
    assert "missing required field: environment" in validate(path)


def test_invalid_environment(tmp_path):
    path = write_config(
        tmp_path,
        {"name": "platform", "region": "us-ashburn-1", "environment": "qa"},
    )
    assert "environment must be one of: dev, staging, prod" in validate(path)
