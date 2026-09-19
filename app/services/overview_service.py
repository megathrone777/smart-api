from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, get_collections, paginate, patch
from app.schemas.overview import HideBody
from app.store.expand_location_ids import expand_location_ids
from app.store.get_all_rooms import get_all_rooms
from app.utils import random_data


def get_report() -> dict[str, Any]:
    data = get_collections(
        [collections.device, collections.building, collections.eventLog]
    )

    devices = data[collections.device]
    buildings = data[collections.building]
    logs = data[collections.eventLog]

    rooms = sum(building.get("totalRooms") or 0 for building in buildings)
    offline = [device for device in devices if device.get("status") == "offline"]
    errors = [log for log in logs if log.get("eventTypeLevel") == "Error"]
    warnings = [log for log in logs if log.get("eventTypeLevel") == "Warning"]
    hidden = [log for log in logs if log.get("archivedStatus") == "archived"]

    return {
        "allActiveEventsNumber": len(
            [log for log in logs if log.get("archivedStatus") == "active"]
        ),
        "allHiddenEventsNumber": len(hidden),
        "numberOfDevices": len(devices),
        "numberOfDevicesOffline": len(offline),
        "numberOfErrors": len(errors),
        "numberOfHiddenErrors": len(
            [log for log in errors if log.get("archivedStatus") == "archived"]
        ),
        "numberOfHiddenWarnings": len(
            [log for log in warnings if log.get("archivedStatus") == "archived"]
        ),
        "numberOfRooms": rooms,
        "numberOfWarnings": len(warnings),
        "unassignedNumberOfRooms": random_data.int_(0, 10),
    }


def get_logs(query: dict[str, Any]) -> dict[str, Any]:
    requested_ids: list[int] = []

    raw_location_ids = query.get("locationId")

    if raw_location_ids:
        for part in raw_location_ids.split(","):
            try:
                value = int(part.strip())
            except (TypeError, ValueError):
                continue

            if value > 0:
                requested_ids.append(value)

    all_logs = get_all(collections.eventLog)
    room_ids = (
        expand_location_ids(requested_ids) if requested_ids else None
    )

    logs = all_logs

    if query.get("activeErrors") == "true":
        logs = [log for log in logs if log.get("eventTypeLevel") == "Error"]
    elif query.get("activeWarnings") == "true":
        logs = [log for log in logs if log.get("eventTypeLevel") == "Warning"]

    event_type_level = query.get("eventTypeLevel")

    if event_type_level:
        logs = [log for log in logs if log.get("eventTypeLevel") == event_type_level]

    want_hidden = query.get("hidden") == "true"

    logs = [
        log
        for log in logs
        if (log.get("archivedStatus") == "archived") == want_hidden
    ]

    if room_ids is not None:
        logs = [log for log in logs if log.get("locationId") in room_ids]

    return paginate(logs, query)


def get_devices_offline(query: dict[str, Any]) -> dict[str, Any]:
    devices = get_all(collections.device)
    offline: list[dict[str, Any]] = []

    for device in devices:
        if device.get("status") != "offline":
            continue

        item = {
            key: value
            for key, value in device.items()
            if key
            not in (
                "batteryLevel",
                "buildingFloorString",
                "deviceMappingId",
                "roomName",
                "temperatureOffset",
            )
        }

        building_floor_string = device.get("buildingFloorString")
        device_mapping_id = device.get("deviceMappingId")
        room_name = device.get("roomName")
        temperature_offset = device.get("temperatureOffset")

        item["batteryLevel"] = (
            "low" if device.get("batteryLevel") == "unbekannt" else device.get("batteryLevel")
        )
        item["buildingFloorString"] = (
            building_floor_string
            if building_floor_string is not None
            else "Gebäude · Etage"
        )
        item["deviceMappingId"] = (
            device_mapping_id if device_mapping_id is not None else 0
        )
        item["locationTags"] = []
        item["roomName"] = room_name if room_name is not None else "-"
        item["temperatureOffset"] = (
            temperature_offset if temperature_offset is not None else 0
        )

        offline.append(item)

    return paginate(offline, query)


def get_unassigned_rooms(query: dict[str, Any]) -> dict[str, Any]:
    rooms = get_all_rooms()
    rows: list[dict[str, Any]] = []

    for room in rooms:
        if room.get("assignedNumberOfRooms") != 0:
            continue

        building_floor_string = room.get("buildingFloorString")
        location_id = room.get("locationId")
        location_tags = room.get("locationTags")
        program_assigned = room.get("programAssigned")

        rows.append(
            {
                "buildingFloorString": (
                    building_floor_string
                    if building_floor_string is not None
                    else "Gebäude · Etage"
                ),
                "id": room.get("id"),
                "locationId": location_id if location_id is not None else room.get("id"),
                "locationTags": location_tags if location_tags is not None else [],
                "name": room.get("name"),
                "tag": program_assigned if program_assigned is not None else "-",
            }
        )

    return paginate(rows, query)


def toggle_log(log_id: str, body: HideBody) -> dict[str, bool]:
    patch(
        collections.eventLog,
        log_id,
        {"archivedStatus": "archived" if body.hide else "active"},
    )

    return {"success": True}
