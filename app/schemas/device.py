from typing import List, Optional

from pydantic import BaseModel


class DeviceBody(BaseModel):
    devEui: Optional[str] = None
    deviceName: Optional[str] = None
    deviceType: Optional[str] = None
    deviceTypeBranded: Optional[str] = None
    locationId: Optional[int] = None
    temperatureOffset: Optional[float] = None


class DeviceNameBody(BaseModel):
    deviceName: Optional[str] = None


class AssignDevicesBody(BaseModel):
    deviceMappingIds: Optional[List[int]] = None
