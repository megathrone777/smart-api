from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, paginate, patch
from app.schemas.energy import MeterBody
from app.utils import random_data, series

CONSUMPTION_RANGES = [
    "consumptionValueNow",
    "last60Minutes",
    "today",
    "week",
    "month",
    "year",
]


def get_meters(query: dict[str, Any]) -> dict[str, Any]:
    meters = get_all(collections.meter)

    energy_source = query.get("energySource")

    if energy_source:
        meters = [
            meter for meter in meters if meter.get("energySource") == energy_source
        ]

    return paginate(meters, query)


def get_consumption_info() -> dict[str, Any]:
    info: dict[str, Any] = {}

    for range_name in CONSUMPTION_RANGES:
        cubic = random_data.float_(0.5, 500, 2)

        info[range_name] = {
            "kwh": random_data.float_(cubic * 9, cubic * 11, 2),
            "m^3": cubic,
            "price": random_data.float_(cubic * 1, cubic * 2, 2),
        }

    return info


def get_meter_chart(query: dict[str, Any]) -> list[dict[str, Any]]:
    meters = get_all(collections.meter)
    requested_ids = query.get("meterIds")
    requested = requested_ids.split(",") if requested_ids else None
    selected = (
        [meter for meter in meters if f"{meter.get('id')}" in requested]
        if requested
        else meters[:3]
    )

    from_ = query.get("dateFrom") or ""
    to_ = query.get("dateTo") or ""

    return [
        {"data": series(from_, to_, 24), "meterName": meter.get("name")}
        for meter in selected
    ]


def get_weather_chart(query: dict[str, Any]) -> list[dict[str, Any]]:
    from_ = query.get("dateFrom") or ""
    to_ = query.get("dateTo") or ""

    return [
        {"createdAt": point["createdAt"], "temperature": random_data.float_(-5, 25)}
        for point in series(from_, to_, 24)
    ]


def update_meter(meter_id: str, body: MeterBody) -> dict[str, Any]:
    changes = body.model_dump(exclude_unset=True)
    changes["updatedAt"] = random_data.now_iso()

    updated_meter = patch(collections.meter, meter_id, changes)

    return updated_meter if updated_meter is not None else {"success": False}
