from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies import pagination
from app.services import operations_service

router = APIRouter()


@router.get("/operationaloverview/{floor_id}/details")
def get_floor_details(floor_id: str):
    return operations_service.get_floor_details(floor_id)


@router.get("/operationaloverview/list")
def get_buildings(searchRoomName: str | None = None):
    return operations_service.get_buildings(searchRoomName)


@router.get("/operationaloverview/tech/list")
def get_tech_rooms(
    query: dict[str, Any] = Depends(pagination),
    hasOccupancies: str | None = None,
    searchname: str | None = None,
):
    return operations_service.get_tech_rooms(
        {**query, "hasOccupancies": hasOccupancies, "searchname": searchname}
    )
