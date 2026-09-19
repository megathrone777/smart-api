from typing import Optional

from pydantic import BaseModel


class TagBody(BaseModel):
    color: Optional[str] = None
    name: Optional[str] = None
