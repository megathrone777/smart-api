from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers.edges import get_edges, remove_edge, remove_edges_many
from app.helpers.get_by_id import get_by_id
from app.helpers.remove import remove
from app.helpers.remove_many import remove_many


def delete_location_by_id(id_: Any) -> bool:
    building = get_by_id(collections.building, id_)

    if building:
        floor_ids = get_edges(f"building:{id_}:floors")
        room_keys = [f"floor:{floor_id}:rooms" for floor_id in floor_ids]
        room_id_lists = [get_edges(key) for key in room_keys]

        remove_many(collections.room, [id_ for ids in room_id_lists for id_ in ids])
        remove_many(collections.floor, floor_ids)
        remove_edges_many([*room_keys, f"building:{id_}:floors"])

        return remove(collections.building, id_)

    room = get_by_id(collections.room, id_)

    if room:
        remove_edge(f"floor:{room.get('parentId')}:rooms", id_)

        return remove(collections.room, id_)

    return False
