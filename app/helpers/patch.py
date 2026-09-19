from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase
from app.globals.id_fields import id_fields
from app.helpers.get_all import _strip_seq


def patch(name: str, id_: Any, changes: dict[str, Any]) -> dict[str, Any] | None:
    response = (
        supabase.table(name)
        .update(changes)
        .eq(id_fields[name], id_)
        .select()
        .execute()
    )
    data = response.data or []

    if not data:
        return None

    return _strip_seq(data[0])
