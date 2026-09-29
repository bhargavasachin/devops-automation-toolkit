"""Tests for python/json_merge.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from json_merge import merge


def test_deep_merge_combines_nested_dicts():
    base = {"a": 1, "nested": {"x": 1, "y": 2}}
    override = {"nested": {"y": 20, "z": 30}}
    assert merge(base, override) == {"a": 1, "nested": {"x": 1, "y": 20, "z": 30}}


def test_right_side_wins_on_scalar_conflict():
    assert merge({"tag": "old"}, {"tag": "new"}) == {"tag": "new"}


def test_non_dict_values_are_replaced_not_merged():
    assert merge({"items": [1, 2]}, {"items": [3]}) == {"items": [3]}
    assert merge({"count": 1}, {"count": "many"}) == {"count": "many"}


def test_missing_keys_are_added():
    assert merge({}, {"region": "us-ashburn-1"}) == {"region": "us-ashburn-1"}
