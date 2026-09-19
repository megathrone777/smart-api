from __future__ import annotations

from typing import Any, Iterable

from app.globals.collections import collections
from app.helpers.get_collections import get_collections


def expand_location_ids(ids: Iterable[Any]) -> set[Any]:
    data = get_collections([collections.floor, collections.room])

    floors = data[collections.floor]
    rooms = data[collections.room]

    room_ids = {room.get("id") for room in rooms}
    floor_ids = {floor.get("id") for floor in floors}
    expanded: set[Any] = set()

    for id_ in ids:
        if id_ in room_ids:
            expanded.add(id_)

            continue

        if id_ in floor_ids:
            expanded.update(
                room.get("id") for room in rooms if room.get("parentId") == id_
            )

            continue

        building_floor_ids = {
            floor.get("id") for floor in floors if floor.get("parentId") == id_
        }

        expanded.update(
            room.get("id") for room in rooms if room.get("parentId") in building_floor_ids
        )

    return expanded
