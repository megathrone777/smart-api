from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase
from app.helpers.get_all import get_all


def get_collections(names: list[str]) -> dict[str, list[dict[str, Any]]]:
    return {name: get_all(name) for name in names}
