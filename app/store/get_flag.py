from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase


def get_flag(field: str) -> Any:
    response = (
        supabase.table("meta")
        .select("value")
        .eq("field", field)
        .maybe_single()
        .execute()
    )

    if not response or not response.data or "value" not in response.data:
        return None

    return response.data["value"]
