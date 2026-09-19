from typing import Optional

from pydantic import BaseModel


class HideBody(BaseModel):
    hide: Optional[bool] = None
