from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import pagination
from app.schemas.location import LocationCreateBody, LocationUpdateBody
from app.services import location_service

router = APIRouter()


@router.delete("/locations/{location_id}")
def delete_location(location_id: str):
    return location_service.delete_location(location_id)


@router.get("/locations")
def get_locations(searchname: str | None = None):
    return location_service.get_locations(searchname)


@router.get("/locations/{floor_id}")
def get_floor_locations(
    floor_id: str, query: dict[str, Any] = Depends(pagination), searchname: str | None = None
):
    return location_service.get_floor_locations(floor_id, {**query, "searchname": searchname})


@router.get("/export/rooms-data")
def export_rooms_data():
    return location_service.export_rooms_data()


@router.post("/locations")
def create_location(body: LocationCreateBody):
    building = location_service.create_location(body)

    return JSONResponse(status_code=201, content=building)


@router.put("/locations")
def update_location(body: LocationUpdateBody):
    return location_service.update_location(body)
