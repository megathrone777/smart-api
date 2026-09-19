from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies import pagination
from app.schemas.overview import HideBody
from app.services import overview_service

router = APIRouter()


@router.get("/overview/report")
def get_report():
    return overview_service.get_report()


@router.get("/overview/list")
def get_logs(
    query: dict[str, Any] = Depends(pagination),
    activeErrors: str | None = None,
    activeWarnings: str | None = None,
    eventTypeLevel: str | None = None,
    hidden: str | None = None,
    locationId: str | None = None,
):
    return overview_service.get_logs(
        {
            **query,
            "activeErrors": activeErrors,
            "activeWarnings": activeWarnings,
            "eventTypeLevel": eventTypeLevel,
            "hidden": hidden,
            "locationId": locationId,
        }
    )


@router.get("/overview/list-devices-offline")
def get_devices_offline(query: dict[str, Any] = Depends(pagination)):
    return overview_service.get_devices_offline(query)


@router.get("/overview/list-unassigned-rooms")
def get_unassigned_rooms(query: dict[str, Any] = Depends(pagination)):
    return overview_service.get_unassigned_rooms(query)


@router.put("/overview/{log_id}")
def toggle_log(log_id: str, body: HideBody):
    return overview_service.toggle_log(log_id, body)
