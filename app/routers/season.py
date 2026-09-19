from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.season import PostcodeBody, SeasonSettingsBody
from app.services import season_service

router = APIRouter()


@router.get("/summer-mode")
def get_locations(buildingName: str | None = None):
    return season_service.get_locations(buildingName)


# Static segment must be matched before "/summer-mode/{location_id}/dwd".
@router.get("/summer-mode/test/dwd")
def verify_postcode(postcode: str | None = None):
    return season_service.verify_postcode(postcode)


@router.get("/summer-mode/{location_id}")
def get_location_details(location_id: str):
    return season_service.get_location_details(location_id)


@router.get("/summer-mode/{location_id}/dwd")
def get_dwd_info(location_id: str):
    return season_service.get_dwd_info(location_id)


@router.put("/summer-mode/{location_id}")
def update_settings(location_id: str, body: SeasonSettingsBody):
    return season_service.update_settings(location_id, body)


@router.put("/summer-mode/{location_id}/toggle")
def toggle_mode(location_id: str):
    return season_service.toggle_mode(location_id)


@router.put("/summer-mode/{location_id}/postcode")
def update_postcode(location_id: str, body: PostcodeBody):
    return season_service.update_postcode(location_id, body)
