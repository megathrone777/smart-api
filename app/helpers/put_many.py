from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase
from app.globals.id_fields import id_fields


def put_many(name: str, entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not entities:
        return entities

    supabase.table(name).upsert(entities, on_conflict=id_fields[name]).execute()

    return entities
