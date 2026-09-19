from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers.get_all import get_all


def get_buildings_tree() -> list[dict[str, Any]]:
    buildings = get_all(collections.building)
    floors = get_all(collections.floor)
    rooms = get_all(collections.room)

    rooms_by_floor: dict[Any, list[dict[str, Any]]] = {}
    for room in rooms:
        rooms_by_floor.setdefault(room.get("parentId"), []).append(room)

    floors_by_building: dict[Any, list[dict[str, Any]]] = {}
    for floor in floors:
        floor["children"] = rooms_by_floor.get(floor.get("id"), [])
        floors_by_building.setdefault(floor.get("parentId"), []).append(floor)

    for building in buildings:
        building["children"] = floors_by_building.get(building.get("id"), [])

    return buildings
