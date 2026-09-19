from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies import pagination
from app.schemas.energy import MeterBody
from app.services import energy_service
from app.utils import random_data, room_chart_points

router = APIRouter()


@router.get("/meters/list")
def get_meters(
    query: dict[str, Any] = Depends(pagination), energySource: str | None = None
):
    return energy_service.get_meters({**query, "energySource": energySource})


@router.get("/meters/{meter_id}/consumption/info")
def get_consumption_info(meter_id: str):
    return energy_service.get_consumption_info()


@router.get("/chart/meters/consumption")
def get_meter_chart(
    dateFrom: str | None = None,
    dateTo: str | None = None,
    meterIds: str | None = None,
):
    return energy_service.get_meter_chart(
        {"dateFrom": dateFrom, "dateTo": dateTo, "meterIds": meterIds}
    )


@router.get("/chart/weather/temperatures")
def get_weather_chart(dateFrom: str | None = None, dateTo: str | None = None):
    return energy_service.get_weather_chart({"dateFrom": dateFrom, "dateTo": dateTo})


@router.get("/chart/room-temperature/{room_id}")
def get_room_temperature_chart(room_id: str):
    return room_chart_points(lambda: random_data.float_(17, 24))


@router.get("/chart/room-humidity/{room_id}")
def get_room_humidity_chart(room_id: str):
    return room_chart_points(lambda: random_data.int_(30, 70))


@router.get("/chart/valve-position/{room_id}")
def get_valve_position_chart(room_id: str):
    return room_chart_points(lambda: random_data.int_(0, 100))


@router.put("/meters/{meter_id}")
def update_meter(meter_id: str, body: MeterBody):
    return energy_service.update_meter(meter_id, body)
