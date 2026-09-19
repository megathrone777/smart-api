from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class LocationCreateBody(BaseModel):
    name: Optional[str] = None
    children: Optional[List[Dict[str, Any]]] = None


class LocationUpdateBody(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
