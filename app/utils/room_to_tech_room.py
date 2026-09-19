from __future__ import annotations

from typing import Any

from app.utils.random_data import bool_, float_, int_, past_date, round_half_up


def room_to_tech_room(room: dict[str, Any]) -> dict[str, Any]:
    target = float_(19, 23)
    current = room.get("roomTemperature")

    if current is None:
        current = float_(17, 24)

    return {
        "buildingName": room.get("buildingName") or "Gebäude",
        "difference": round_half_up((current - target) * 10) / 10,
        "floorName": room.get("floorName") or "Etage",
        "hasOccupancies": bool(room.get("hasOccupancy") or False),
        "heatingScheduleId": int_(1001, 1099) if bool_(0.6) else None,
        "isOccupied": bool(room.get("isOccupied") or False),
        "locationId": room.get("id"),
        "locationTags": room.get("locationTags") or [],
        "roomName": room.get("name"),
        "roomTemperature": current,
        "targetTemperature": target,
        "timestamp": past_date(120),
    }
