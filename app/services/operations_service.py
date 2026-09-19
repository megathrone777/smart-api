from __future__ import annotations

from typing import Any

from app.store.get_all_rooms import get_all_rooms
from app.store.get_buildings_tree import get_buildings_tree
from app.store.get_floor_rooms import get_floor_rooms
from app.utils import room_to_tech_room


def get_buildings(search_room_name: str | None) -> list[dict[str, Any]]:
    buildings = get_buildings_tree()

    if not search_room_name:
        return buildings

    needle = search_room_name.lower()
    result: list[dict[str, Any]] = []

    for building in buildings:
        filtered_floors = []
        for floor in building.get("children") or []:
            filtered_rooms = [
                room
                for room in floor.get("children") or []
                if needle in f"{room.get('name')}".lower()
            ]
            filtered_floors.append({**floor, "children": filtered_rooms})

        result.append({**building, "children": filtered_floors})

    return [
        building
        for building in result
        if any(floor.get("children") for floor in building.get("children") or [])
    ]


def get_floor_details(floor_id: str) -> dict[str, list[dict[str, Any]]]:
    rooms = get_floor_rooms(floor_id)

    return {"rooms": [room_to_tech_room(room) for room in rooms]}


def get_tech_rooms(query: dict[str, Any]) -> dict[str, Any]:
    from app.helpers.paginate import paginate

    rooms = get_all_rooms()

    searchname = query.get("searchname")

    if searchname:
        needle = searchname.lower()
        rooms = [room for room in rooms if needle in f"{room.get('name')}".lower()]

    tech_rooms = [room_to_tech_room(room) for room in rooms]

    if query.get("hasOccupancies") == "true":
        tech_rooms = [room for room in tech_rooms if room.get("hasOccupancies")]

    page = paginate(tech_rooms, query)

    return {
        "count": page["count"],
        "hasAnyOccupancies": any(room.get("hasOccupancies") for room in tech_rooms),
        "rows": page["rows"],
    }
