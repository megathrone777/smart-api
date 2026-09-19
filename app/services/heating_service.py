from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.globals.weekdays import weekdays
from app.helpers import get_all, get_by_id, patch, put, remove
from app.schemas.heating import ProgramBody
from app.store.get_buildings_tree import get_buildings_tree
from app.utils import random_data


def make_program_days(heating_schedule_id: Any) -> list[dict[str, Any]]:
    days: list[dict[str, Any]] = []

    for weekday in weekdays:
        days.append(
            {
                "day": weekday["day"],
                "dayName": weekday["dayName"],
                "from": "06:00",
                "heatingScheduleId": heating_schedule_id,
                "targetTemperature": random_data.float_(20, 22),
                "to": "18:00",
            }
        )
        days.append(
            {
                "day": weekday["day"],
                "dayName": weekday["dayName"],
                "from": "18:00",
                "heatingScheduleId": heating_schedule_id,
                "targetTemperature": random_data.float_(16, 18),
                "to": "06:00",
            }
        )

    return days


def get_programs() -> list[dict[str, Any]]:
    return get_all(collections.program)


def get_program_by_id(heating_schedule_id: str) -> dict[str, Any]:
    program = get_by_id(collections.program, heating_schedule_id)

    return program if program is not None else {"success": False}


def get_program_details(heating_schedule_id: str) -> dict[str, Any]:
    programs = get_all(collections.program)
    buildings = get_buildings_tree()

    program = next(
        (
            item
            for item in programs
            if f"{item.get('id')}" == heating_schedule_id
        ),
        None,
    )

    if program is None and programs:
        program = programs[0]

    id_ = program.get("id") if program else None

    if id_ is None:
        id_ = int(heating_schedule_id)

    assigned_rooms = random_data.pick_some(buildings, 1, 2)

    def default(value: Any, fallback: Any) -> Any:
        return value if value is not None else fallback

    return {
        "allowDeviceOverride": default(
            program.get("allowDeviceOverride") if program else None, False
        ),
        "assignedRooms": assigned_rooms,
        "days": make_program_days(id_),
        "deviceOverrideTemperatureMax": default(
            program.get("deviceOverrideTemperatureMax") if program else None, 26
        ),
        "deviceOverrideTemperatureMin": default(
            program.get("deviceOverrideTemperatureMin") if program else None, 16
        ),
        "id": id_,
        "locations": [building["id"] for building in assigned_rooms],
        "templateName": default(
            program.get("templateName") if program else None, "Heizplan"
        ),
        "updatedAt": default(
            program.get("updatedAt") if program else None, random_data.now_iso()
        ),
    }


def create_program(body: dict[str, Any]) -> dict[str, Any]:
    template_name = body.get("templateName")

    program: dict[str, Any] = {
        "allowDeviceOverride": False,
        "assignedRooms": 0,
        "deviceOverrideTemperatureMax": 26,
        "deviceOverrideTemperatureMin": 16,
        "id": random_data.next_id(),
        "templateName": template_name
        if template_name is not None
        else f"Neuer Heizplan {random_data.int_(1, 999)}",
        "updatedAt": random_data.now_iso(),
    }

    put(collections.program, program)

    return program


def update_program_by_id(heating_schedule_id: str, body: ProgramBody) -> dict[str, Any]:
    changes = body.model_dump(exclude_unset=True)
    changes["updatedAt"] = random_data.now_iso()

    updated = patch(collections.program, heating_schedule_id, changes)

    return updated if updated is not None else {"success": False}


def delete_program_by_id(heating_schedule_id: str) -> dict[str, bool]:
    remove(collections.program, heating_schedule_id)

    return {"success": True}
