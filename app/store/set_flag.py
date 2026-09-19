from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase


def set_flag(field: str, value: Any) -> None:
    supabase.table("meta").upsert({"field": field, "value": value}).execute()
