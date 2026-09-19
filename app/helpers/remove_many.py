from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase
from app.globals.id_fields import id_fields


def remove_many(name: str, ids: list[Any]) -> int:
    if not ids:
        return 0

    response = (
        supabase.table(name)
        .delete(count="exact")
        .in_(id_fields[name], ids)
        .execute()
    )

    return response.count or 0
