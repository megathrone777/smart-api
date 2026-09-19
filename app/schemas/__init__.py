from app.schemas.auth import LoginBody, RegisterBody
from app.schemas.device import AssignDevicesBody, DeviceBody, DeviceNameBody
from app.schemas.energy import MeterBody
from app.schemas.heating import ProgramBody, ProgramCreateBody
from app.schemas.location import LocationCreateBody, LocationUpdateBody
from app.schemas.notifications import RuleBody, SystemActivationBody
from app.schemas.occupancy import (
    OccupancySettingsBody,
    PresenceStatusBody,
    PresenceTemperatureBody,
    TimeslotBody,
)
from app.schemas.overview import HideBody
from app.schemas.season import PostcodeBody, SeasonSettingsBody
from app.schemas.tag import TagBody
from app.schemas.user import NotificationsToggleBody, UserBody, UserRole

__all__ = [
    "AssignDevicesBody",
    "DeviceBody",
    "DeviceNameBody",
    "HideBody",
    "LocationCreateBody",
    "LocationUpdateBody",
    "LoginBody",
    "MeterBody",
    "NotificationsToggleBody",
    "OccupancySettingsBody",
    "PostcodeBody",
    "PresenceStatusBody",
    "PresenceTemperatureBody",
    "ProgramBody",
    "ProgramCreateBody",
    "RegisterBody",
    "RuleBody",
    "SeasonSettingsBody",
    "SystemActivationBody",
    "TagBody",
    "TimeslotBody",
    "UserBody",
    "UserRole",
]
