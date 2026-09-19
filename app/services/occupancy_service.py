from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, paginate, patch, put, remove
from app.schemas.occupancy import (
    OccupancySettingsBody,
    PresenceStatusBody,
    PresenceTemperatureBody,
    TimeslotBody,
)
from app.utils import empty_conflict, random_data


def get_occupancy_locations(query: dict[str, Any]) -> dict[str, Any]:
    rows = get_all(collections.occupancySetting)

    searchname = query.get("searchname")

    if searchname:
        needle = searchname.lower()
        rows = [row for row in rows if needle in f"{row.get('roomName')}".lower()]

    return paginate(rows, query)


def get_presence_locations(query: dict[str, Any]) -> dict[str, Any]:
    rows = get_all(collections.presence)

    searchname = query.get("searchname")

    if searchname:
        needle = searchname.lower()
        rows = [row for row in rows if needle in f"{row.get('roomName')}".lower()]

    status = query.get("status")

    if status:
        rows = [row for row in rows if row.get("status") == status]

    return paginate(rows, query)


def get_upcoming_locations(query: dict[str, Any]) -> dict[str, Any]:
    rows = get_all(collections.upcoming)

    searchname = query.get("searchname")

    if searchname:
        needle = searchname.lower()
        rows = [row for row in rows if needle in f"{row.get('roomName')}".lower()]

    status = query.get("status")

    if status:
        rows = [row for row in rows if row.get("status") == status]

    return paginate(rows, query)


def get_uploads(query: dict[str, Any]) -> dict[str, Any]:
    rows = get_all(collections.upload)

    return paginate(rows, query)


def create_timeslot(body: TimeslotBody) -> dict[str, Any]:
    data = body.model_dump(exclude_unset=True, by_alias=True)

    def value(key: str) -> Any:
        return data.get(key)

    slot: dict[str, Any] = {
        "buildingName": value("buildingName")
        if value("buildingName") is not None
        else "Gebäude",
        "date": value("date") if value("date") is not None else random_data.date_only(1),
        "floorName": value("floorName")
        if value("floorName") is not None
        else "Etage",
        "from": value("from") if value("from") is not None else "08:00",
        "id": random_data.next_id(),
        "locationId": value("locationId")
        if value("locationId") is not None
        else random_data.int_(1001, 1099),
        "locationTags": value("locationTags")
        if value("locationTags") is not None
        else [],
        "roomName": value("roomName") if value("roomName") is not None else "Raum",
        "settings": value("settings")
        if value("settings") is not None
        else {
            "allowDeviceOverride": False,
            "deviceOverrideTemperatureMax": None,
            "deviceOverrideTemperatureMin": None,
        },
        "status": value("status") if value("status") is not None else "occupied",
        "tagId": value("tagId")
        if value("tagId") is not None
        else {"color": "blue", "name": "Tag"},
        "targetTemperature": value("targetTemperature")
        if value("targetTemperature") is not None
        else 21,
        "to": value("to") if value("to") is not None else "17:00",
    }

    put(collections.upcoming, slot)

    return slot


def update_timeslot(occupancy_id: str, body: TimeslotBody) -> dict[str, Any]:
    updated_timeslot = patch(
        collections.upcoming,
        occupancy_id,
        body.model_dump(exclude_unset=True, by_alias=True),
    )

    return updated_timeslot if updated_timeslot is not None else {"success": False}


def delete_timeslot(occupancy_id: str) -> dict[str, bool]:
    remove(collections.upcoming, occupancy_id)

    return {"success": True}


def update_occupancy_settings(
    body: OccupancySettingsBody, location_ids: list[str]
) -> dict[str, bool]:
    changes = body.model_dump(exclude_unset=True)

    for id_ in location_ids:
        patch(collections.occupancySetting, id_, changes)

    return {"success": True}


def update_presence_status(
    location_id: str, body: PresenceStatusBody
) -> dict[str, Any]:
    if body.status:
        updated_location = patch(
            collections.presence,
            location_id,
            {"status": body.status, "statusChangedAt": random_data.now_iso()},
        )
    else:
        updated_location = None

    return updated_location if updated_location is not None else {"success": False}


def update_presence_temperature(
    location_id: str, body: PresenceTemperatureBody
) -> dict[str, Any]:
    if "targetTemperature" in body.model_fields_set:
        updated_location = patch(
            collections.presence,
            location_id,
            {
                "currentTargetTemperature": body.targetTemperature,
                "temporaryTargetTemperature": body.targetTemperature,
            },
        )
    else:
        updated_location = None

    return updated_location if updated_location is not None else {"success": False}


def check_conflict(action: str = "create") -> dict[str, Any]:
    return empty_conflict(action)
