from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase


def get_flag(field: str) -> Any:
    # maybe_single() returns the row dict (or None) directly, like supabase-js.
    data = (
        supabase.table("meta")
        .select("value")
        .eq("field", field)
        .maybe_single()
        .execute()
    )

    if not data or "value" not in data:
        return None

    return data["value"]
