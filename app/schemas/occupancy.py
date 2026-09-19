from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class TimeslotBody(BaseModel):
    # Fields read by create/update timeslot handlers (POST/PUT occupancy)
    buildingName: Optional[str] = None
    date: Optional[str] = None
    floorName: Optional[str] = None
    from_: Optional[str] = Field(default=None, alias="from")
    locationId: Optional[int] = None
    locationTags: Optional[List[Any]] = None
    roomName: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    status: Optional[Literal["occupied", "unoccupied"]] = None
    tagId: Optional[Any] = None
    targetTemperature: Optional[float] = None
    to: Optional[str] = None

    model_config = {"populate_by_name": True}


class OccupancySettingsBody(BaseModel):
    allowDeviceOverride: Optional[bool] = None
    deviceOverrideTemperatureMax: Optional[float] = None
    deviceOverrideTemperatureMin: Optional[float] = None
    locationId: Optional[int] = None
    mode: Optional[Literal["planning", "presence"]] = None
    occupiedTargetTemperature: Optional[float] = None
    unoccupiedTargetTemperature: Optional[float] = None


class PresenceStatusBody(BaseModel):
    status: Optional[Literal["occupied", "unoccupied"]] = None


class PresenceTemperatureBody(BaseModel):
    targetTemperature: Optional[float] = None
