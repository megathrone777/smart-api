from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.globals.product_types import product_types
from app.helpers import get_all, paginate, patch, put
from app.schemas.device import DeviceBody, DeviceNameBody
from app.utils import random_data


def get_devices(query: dict[str, Any]) -> dict[str, Any]:
    devices = get_all(collections.device)

    search_value = query.get("searchValue")

    if search_value:
        needle = search_value.lower()
        devices = [
            device
            for device in devices
            if needle in f"{device.get('deviceName')}".lower()
            or needle in f"{device.get('devEui')}".lower()
        ]

    status = query.get("status")

    if status:
        statuses = status.split(",")
        devices = [device for device in devices if device.get("status") in statuses]

    battery_level = query.get("batteryLevel")

    if battery_level:
        levels = battery_level.split(",")
        devices = [
            device for device in devices if device.get("batteryLevel") in levels
        ]

    filter_product_types = query.get("filterProductTypes")

    if filter_product_types:
        types = filter_product_types.split(",")
        devices = [device for device in devices if device.get("deviceType") in types]

    connection_quality = query.get("connectionQuality")

    if connection_quality:
        qualities = connection_quality.split(",")
        devices = [
            device
            for device in devices
            if device.get("connectionQuality") in qualities
        ]

    location_id = query.get("locationId")

    if location_id:
        ids = location_id.split(",")
        devices = [
            device
            for device in devices
            if device.get("locationId") is not None
            and f"{device.get('locationId')}" in ids
        ]

    return paginate(devices, query)


def get_product_types() -> list[dict[str, str]]:
    return product_types


def get_connection_qualities() -> list[dict[str, str]]:
    qualities = ["bad", "OK", "good", "optimal", "pending"]

    return [
        {"connectionQuality": quality, "spreadingFactor": f"SF{7 + index}"}
        for index, quality in enumerate(qualities)
    ]


def get_device_details() -> dict[str, Any]:
    child_lock = random_data.bool_(0.3)
    details: dict[str, Any] = {
        "currentHumidity": random_data.int_(30, 70),
        "currentTemperature": random_data.float_(17, 24),
        "lightIntensity": random_data.int_(0, 1000),
        "movementDetected": random_data.bool_(0.3),
        "openClose": "open" if random_data.bool_(0.2) else "closed",
        "targetTemperature": random_data.float_(18, 23),
        "timestamp": random_data.past_date(60),
        "valvePositionInPercent": f"{random_data.int_(0, 100)}",
        "windowOpenStatus": random_data.bool_(0.15),
    }

    if child_lock:
        details = {"childLock": True, **details}

    return details


def get_unused_device(identifier: str | None) -> dict[str, str]:
    product = random_data.pick(product_types)

    return {
        "devEui": identifier if identifier is not None else random_data.dev_eui(),
        "deviceType": product["productType"],
        "externalName": product["externalName"],
        "productType": product["productType"],
    }


def create_device(body: DeviceBody) -> dict[str, Any]:
    device: dict[str, Any] = {
        "batteryLevel": "full",
        "buildingFloorString": None,
        "connectionQuality": "pending",
        "devEui": body.devEui if body.devEui is not None else random_data.dev_eui(),
        "deviceId": f"dev-{random_data.hex_(8)}",
        "deviceMappingId": random_data.next_id(),
        "deviceName": body.deviceName
        if body.deviceName is not None
        else f"Neues Gerät {random_data.int_(1, 999)}",
        "deviceType": body.deviceType
        if body.deviceType is not None
        else "vicki-lorawan",
        "deviceTypeBranded": body.deviceTypeBranded
        if body.deviceTypeBranded is not None
        else "mclimate-vicki",
        "gatewayMappingId": None,
        "isController": False,
        "lastSeen": random_data.now_iso(),
        "locationId": None,
        "roomName": None,
        "status": "online",
        "temperatureOffset": None,
    }

    put(collections.device, device)

    return device


def assign_devices(location_id: str, device_mapping_ids: list[int]) -> dict[str, bool]:
    for mapping_id in device_mapping_ids:
        patch(collections.device, mapping_id, {"locationId": int(location_id)})

    return {"success": True}


def update_device_name(device_id: str, body: DeviceNameBody) -> dict[str, bool]:
    changes = {"deviceName": body.deviceName} if body.deviceName is not None else {}

    updated_device = patch(collections.device, device_id, changes)

    return {"success": updated_device is not None}
