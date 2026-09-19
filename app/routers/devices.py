from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import pagination
from app.globals.product_types import product_types
from app.schemas.device import AssignDevicesBody, DeviceBody, DeviceNameBody
from app.services import device_service

router = APIRouter()


@router.get("/devicemanagement/list")
def get_devices(
    query: dict[str, Any] = Depends(pagination),
    batteryLevel: str | None = None,
    connectionQuality: str | None = None,
    filterProductTypes: str | None = None,
    locationId: str | None = None,
    searchValue: str | None = None,
    status: str | None = None,
):
    return device_service.get_devices(
        {
            **query,
            "batteryLevel": batteryLevel,
            "connectionQuality": connectionQuality,
            "filterProductTypes": filterProductTypes,
            "locationId": locationId,
            "searchValue": searchValue,
            "status": status,
        }
    )


@router.get("/devicemanagement/producttypes")
def get_product_types():
    return device_service.get_product_types()


@router.get("/devicemanagement/connectionqualities")
def get_connection_qualities():
    return device_service.get_connection_qualities()


@router.get("/devicemanagement/lastpayload")
def get_device_details():
    return device_service.get_device_details()


@router.get("/devicemanagement/device/lookup-unused")
def get_unused_device(identifier: str | None = None):
    return device_service.get_unused_device(identifier)


@router.post("/devicemanagement/devices")
def create_device(body: DeviceBody):
    device = device_service.create_device(body)

    return JSONResponse(status_code=201, content=device)


@router.post("/devicemanagement/location/{location_id}/assign")
def assign_devices(location_id: str, body: AssignDevicesBody):
    return device_service.assign_devices(location_id, body.deviceMappingIds or [])


@router.post("/devicemanagement/location/{location_id}/gateway/assign")
def assign_gateway(location_id: str):
    return {"success": True}


@router.put("/devicemanagement/devicename/{device_id}")
def update_device_name(device_id: str, body: DeviceNameBody):
    return device_service.update_device_name(device_id, body)


@router.put("/settings/device/{device_mapping_id}")
def update_device_settings(device_mapping_id: str):
    return {"success": True}


@router.put("/settings/gateway/{gateway_mapping_id}")
def update_gateway_settings(gateway_mapping_id: str):
    return {"success": True}
