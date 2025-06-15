"""Utility functions for config and parsing."""

import json


def load_json_file(filename, default=None):
    """Load JSON file or return default."""
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def parse_bool(value, default=False):
    """Parse boolean from string."""
    if value is None:
        return default
    return str(value).lower() in ("1", "true", "yes", "on")


def parse_csv(value, default=None):
    """Parse comma-separated string to list."""
    if not value:
        return default or []
    return [v.strip() for v in value.split(",") if v.strip()]


def find_org_by_chinese_name(org_list, chinese_name):
    """Find organization by Chinese name."""
    if not chinese_name:
        return None
    for org in org_list:
        if org.get("chineseName") == chinese_name:
            return org
    return None
