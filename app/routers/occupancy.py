from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.dependencies import pagination
from app.schemas.occupancy import (
    OccupancySettingsBody,
    PresenceStatusBody,
    PresenceTemperatureBody,
    TimeslotBody,
)
from app.services import occupancy_service
from app.utils import empty_conflict

router = APIRouter()


@router.get("/heatingschedule/occupancy/settings/list")
def get_occupancy_settings(
    query: dict[str, Any] = Depends(pagination), searchname: str | None = None
):
    return occupancy_service.get_occupancy_locations({**query, "searchname": searchname})


@router.get("/heatingschedule/occupancy/presence/rooms")
def get_presence_locations(
    query: dict[str, Any] = Depends(pagination),
    searchname: str | None = None,
    status: str | None = None,
):
    return occupancy_service.get_presence_locations(
        {**query, "searchname": searchname, "status": status}
    )


@router.get("/heatingschedule/occupancy/upcoming/list")
def get_upcoming_locations(
    query: dict[str, Any] = Depends(pagination),
    searchname: str | None = None,
    status: str | None = None,
):
    return occupancy_service.get_upcoming_locations(
        {**query, "searchname": searchname, "status": status}
    )


@router.get("/heatingschedule/occupancy/uploads/list")
def get_uploads(query: dict[str, Any] = Depends(pagination)):
    return occupancy_service.get_uploads(query)


@router.post("/heatingschedule/occupancy/check")
def check_conflict():
    return empty_conflict("create")


@router.post("/heatingschedule/occupancy/import/check")
def check_import_conflict():
    return empty_conflict("create")


@router.post("/heatingschedule/occupancy/import")
def import_occupancy():
    return {"success": True}


@router.post("/heatingschedule/occupancy")
def create_timeslot(body: TimeslotBody):
    slot = occupancy_service.create_timeslot(body)

    return JSONResponse(status_code=201, content=slot)


# Static "settings" path must be matched before "/{occupancy_id}".
@router.put("/heatingschedule/occupancy/settings")
def update_occupancy_settings(request: Request, body: OccupancySettingsBody):
    query_params = request.query_params
    raw = (
        query_params.getlist("locationIds[]")
        or query_params.getlist("locationIds")
    )

    return occupancy_service.update_occupancy_settings(body, list(raw))


@router.put("/heatingschedule/occupancy/{occupancy_id}")
def update_timeslot(occupancy_id: str, body: TimeslotBody):
    return occupancy_service.update_timeslot(occupancy_id, body)


@router.put("/heatingschedule/occupancy/presence/rooms/{location_id}/status")
def update_presence_status(location_id: str, body: PresenceStatusBody):
    return occupancy_service.update_presence_status(location_id, body)


@router.put("/heatingschedule/occupancy/presence/rooms/{location_id}/target-temperature")
def update_presence_temperature(location_id: str, body: PresenceTemperatureBody):
    return occupancy_service.update_presence_temperature(location_id, body)


@router.delete("/heatingschedule/occupancy/{occupancy_id}")
def delete_timeslot(occupancy_id: str):
    return occupancy_service.delete_timeslot(occupancy_id)
