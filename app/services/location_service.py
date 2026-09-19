from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import paginate, patch
from app.schemas.location import LocationCreateBody, LocationUpdateBody
from app.store.delete_location_by_id import delete_location_by_id
from app.store.get_all_rooms import get_all_rooms
from app.store.get_buildings_tree import get_buildings_tree
from app.store.get_floor_rooms import get_floor_rooms
from app.store.save_building_tree import save_building_tree
from app.utils import random_data


def get_locations(searchname: str | None) -> list[dict[str, Any]]:
    buildings = get_buildings_tree()

    if searchname:
        needle = searchname.lower()
        return [
            building
            for building in buildings
            if needle in f"{building.get('name')}".lower()
        ]

    return buildings


def get_floor_locations(
    floor_id: str, query: dict[str, Any]
) -> dict[str, Any]:
    rooms = get_floor_rooms(floor_id)

    searchname = query.get("searchname")

    if searchname:
        search_term = searchname.lower()
        rooms = [room for room in rooms if search_term in f"{room.get('name')}".lower()]

    return paginate(rooms, query)


def create_location(body: LocationCreateBody) -> dict[str, Any]:
    buildings = get_buildings_tree()
    id_ = random_data.next_id()
    children = body.children if body.children is not None else []

    building: dict[str, Any] = {
        "assignedNumberOfRooms": 0,
        "children": children,
        "completedFloors": 0,
        "id": id_,
        "name": body.name if body.name is not None else f"Neues Gebäude {id_}",
        "numberOfDevices": 0,
        "numberOfDevicesOnline": 0,
        "numberOfFloors": len(children),
        "numberOfRooms": 0,
        "parentId": None,
        "roomsAssigned": 0,
        "tag": "blue",
        "totalRooms": 0,
        "type": "building",
        "y": len(buildings),
    }

    save_building_tree(building)

    return building


def update_location(body: LocationUpdateBody) -> dict[str, bool]:
    if body.id and body.name:
        patch(collections.room, body.id, {"name": body.name})

    return {"success": True}


def delete_location(location_id: str) -> dict[str, bool]:
    delete_location_by_id(location_id)

    return {"success": True}


def export_rooms_data() -> dict[str, list[dict[str, Any]]]:
    return {"rows": get_all_rooms()}
