from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase
from app.globals.id_fields import id_fields
from app.helpers.get_all import _strip_seq


def get_by_id(name: str, id_: Any) -> dict[str, Any] | None:
    # supabase-py's maybe_single() returns the row dict (or None) directly,
    # mirroring supabase-js.
    data = (
        supabase.table(name)
        .select("*")
        .eq(id_fields[name], id_)
        .maybe_single()
        .execute()
    )

    if not data:
        return None

    return _strip_seq(data)
