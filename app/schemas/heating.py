from typing import Optional

from pydantic import BaseModel


class ProgramCreateBody(BaseModel):
    templateName: Optional[str] = None


class ProgramBody(BaseModel):
    allowDeviceOverride: Optional[bool] = None
    deviceOverrideTemperatureMax: Optional[float] = None
    deviceOverrideTemperatureMin: Optional[float] = None
    templateName: Optional[str] = None
