from typing import Any, List, Optional

from pydantic import BaseModel


class RuleBody(BaseModel):
    active: Optional[bool] = None
    scheduleTimeFrom: Optional[str] = None
    scheduleTimeTo: Optional[str] = None
    scheduleWeekdays: Optional[List[int]] = None
    tags: Optional[List[Any]] = None
    threshold: Optional[float] = None
    thresholdMinutes: Optional[float] = None
    userId: Optional[int] = None


class SystemActivationBody(BaseModel):
    enabled: Optional[bool] = None
