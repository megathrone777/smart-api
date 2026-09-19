from typing import Any, List, Literal, Optional

from pydantic import BaseModel

UserRole = Literal["admin", "manager", "operator", "superAdmin", "technician"]


class UserBody(BaseModel):
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    locations: Optional[List[Any]] = None
    notificationsEnabled: Optional[bool] = None
    role: Optional[UserRole] = None


class NotificationsToggleBody(BaseModel):
    """Used by PUT /notifications/enabled and POST /notifications/:id/activation."""

    notificationsEnabled: Optional[bool] = None
