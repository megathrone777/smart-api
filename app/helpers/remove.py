from __future__ import annotations

from typing import Any

from app.helpers.remove_many import remove_many


def remove(name: str, id_: Any) -> bool:
    return remove_many(name, [id_]) > 0
