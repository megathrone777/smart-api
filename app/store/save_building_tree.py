from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers.edges import EdgeSet, set_edges_many
from app.helpers.put_many import put_many


def save_building_tree(building: dict[str, Any]) -> None:
    floors = building.get("children") or []
    building_scalars = {key: value for key, value in building.items() if key != "children"}

    floor_scalars: list[dict[str, Any]] = []
    rooms: list[dict[str, Any]] = []
    edge_sets = [EdgeSet(f"building:{building['id']}:floors", [floor["id"] for floor in floors])]

    for floor in floors:
        floor_rooms = floor.get("children") or []

        floor_scalars.append({key: value for key, value in floor.items() if key != "children"})
        rooms.extend(floor_rooms)
        edge_sets.append(EdgeSet(f"floor:{floor['id']}:rooms", [room["id"] for room in floor_rooms]))

    put_many(collections.building, [building_scalars])
    put_many(collections.floor, floor_scalars)
    put_many(collections.room, rooms)
    set_edges_many(edge_sets)
