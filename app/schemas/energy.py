from typing import Optional

from pydantic import BaseModel


class MeterBody(BaseModel):
    brand: Optional[str] = None
    brandType: Optional[str] = None
    conversionFactor: Optional[float] = None
    energySource: Optional[str] = None
    fuelValue: Optional[float] = None
    idFromMeter: Optional[str] = None
    name: Optional[str] = None
    pricePerKwh: Optional[float] = None
    startingValueM3: Optional[float] = None
    stateNumber: Optional[float] = None
