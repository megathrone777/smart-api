from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.notifications import RuleBody, SystemActivationBody
from app.schemas.user import NotificationsToggleBody
from app.services import notification_service

router = APIRouter()


@router.delete("/notifications/rules/room-temperature/{id}")
def delete_room_temperature_rule(id: str):
    return notification_service.delete_rule(id)


@router.delete("/notifications/rules/window-open-duration/{id}")
def delete_window_open_duration_rule(id: str):
    return notification_service.delete_rule(id)


@router.get("/notifications/rules")
def get_rules(source: str | None = None):
    return notification_service.get_rules(source)


@router.get("/notifications/system-activations")
def get_system_activations():
    return notification_service.get_system_activations()


@router.get("/notifications/activations")
def get_user_activations(
    page: str | None = None,
    limit: str | None = None,
    name: str | None = None,
    roles: str | None = None,
):
    return notification_service.get_user_activations(
        {"page": page, "limit": limit, "name": name, "roles": roles}
    )


@router.post("/notifications/{id}/activation")
def update_user_activation(id: str, body: NotificationsToggleBody):
    return notification_service.update_user_activation(id, body)


@router.post("/notifications/rules/room-temperature")
def create_room_temperature_rule(body: RuleBody):
    rule = notification_service.create_rule("aboveThreshold", body)

    return JSONResponse(status_code=201, content=rule)


@router.post("/notifications/rules/window-open-duration")
def create_window_open_duration_rule(body: RuleBody):
    rule = notification_service.create_rule("windowOpenDuration", body)

    return JSONResponse(status_code=201, content=rule)


@router.put("/notifications/system-activations/{event_type}")
def update_system_activation(event_type: str, body: SystemActivationBody):
    return notification_service.update_system_activation(event_type, body)


@router.put("/notifications/rules/room-temperature/{id}")
def update_room_temperature_rule(id: str, body: RuleBody):
    return notification_service.update_rule(id, body)


@router.put("/notifications/rules/window-open-duration/{id}")
def update_window_open_duration_rule(id: str, body: RuleBody):
    return notification_service.update_rule(id, body)


@router.put("/notifications/enabled")
def toggle_notifications(body: NotificationsToggleBody):
    return notification_service.toggle_notifications(body)
