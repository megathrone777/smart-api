from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, get_by_id, patch
from app.schemas.season import PostcodeBody, SeasonSettingsBody
from app.utils import make_dwd


def get_locations(building_name_query: str | None) -> dict[str, Any]:
    locations = get_all(collections.season)

    if building_name_query:
        needle = building_name_query.lower()
        locations = [
            location
            for location in locations
            if needle in f"{location.get('locationName')}".lower()
        ]

    return {
        "activeSummerModeCount": len(
            [location for location in locations if location.get("isActive")]
        ),
        "buildings": locations,
        "totalBuildings": len(locations),
    }


def get_location_details(location_id: str) -> dict[str, Any]:
    location = get_by_id(collections.season, location_id)

    if location:
        return location

    locations = get_all(collections.season)

    return locations[0] if locations else {"success": False}


def get_dwd_info(location_id: str) -> dict[str, Any]:
    location = get_by_id(collections.season, location_id)

    if location is not None and location.get("dwd") is not None:
        return location["dwd"]

    threshold = 15

    if location is not None and location.get("heatingThreshold") is not None:
        threshold = location["heatingThreshold"]

    return make_dwd(threshold)


def toggle_mode(location_id: str) -> dict[str, Any]:
    location = get_by_id(collections.season, location_id)
    current = location.get("isActive") if location else None

    if current is None:
        current = False

    is_active = not current

    if location:
        patch(collections.season, location_id, {"isActive": is_active})

    return {"isActive": is_active}


def update_settings(location_id: str, body: SeasonSettingsBody) -> dict[str, Any]:
    updated_location = patch(
        collections.season, location_id, body.model_dump(exclude_unset=True)
    )

    return updated_location if updated_location is not None else {"success": False}


def update_postcode(location_id: str, body: PostcodeBody) -> dict[str, bool]:
    if "postcode" in body.model_fields_set:
        patch(collections.season, location_id, {"postcode": body.postcode})

    return {"success": True}


def verify_postcode(postcode_query: str | None) -> dict[str, Any]:
    return make_dwd(15)
