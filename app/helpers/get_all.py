from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase


def _strip_seq(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "seq"}


def get_all(name: str) -> list[dict[str, Any]]:
    response = supabase.table(name).select("*").order("seq").execute()

    return [_strip_seq(row) for row in (response.data or [])]
