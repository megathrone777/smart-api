from __future__ import annotations

from typing import Any

from app.globals.id_fields import id_fields
from app.helpers.put_many import put_many


def put(name: str, entity: dict[str, Any]) -> dict[str, Any]:
    put_many(name, [entity])

    return entity
