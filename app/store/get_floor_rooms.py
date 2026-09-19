from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers.get_by_id import get_by_id
from app.helpers.get_collections import get_collections


def get_floor_rooms(floor_id: Any) -> list[dict[str, Any]]:
    floor = get_by_id(collections.floor, floor_id)

    if not floor:
        return []

    rooms = get_all(collections.room)

    return [room for room in rooms if f"{room.get('parentId')}" == f"{floor_id}"]
