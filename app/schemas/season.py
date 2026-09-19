from typing import Literal, Optional

from pydantic import BaseModel


class SeasonSettingsBody(BaseModel):
    heatingThreshold: Optional[float] = None
    isActive: Optional[bool] = None
    mode: Optional[Literal["automatic", "manual"]] = None
    postcode: Optional[str] = None
    targetTemperature: Optional[float] = None


class PostcodeBody(BaseModel):
    postcode: Optional[str] = None
