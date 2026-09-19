from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, paginate, patch, put, remove
from app.schemas.notifications import RuleBody, SystemActivationBody
from app.schemas.user import NotificationsToggleBody
from app.store.set_flag import set_flag
from app.utils import notifications_enabled, random_data


def get_rules(source: str | None) -> dict[str, Any]:
    rules = get_all(collections.rule)
    enabled = notifications_enabled()

    room_temperature = [
        rule
        for rule in rules
        if rule.get("type") in ("aboveThreshold", "belowThreshold")
    ]
    window_open_duration = [
        rule for rule in rules if rule.get("type") == "windowOpenDuration"
    ]

    if source == "roomTemperature":
        return {
            "notificationsEnabled": enabled,
            "roomTemperature": room_temperature,
            "windowOpenDuration": [],
        }

    if source == "windowOpenDuration":
        return {
            "notificationsEnabled": enabled,
            "roomTemperature": [],
            "windowOpenDuration": window_open_duration,
        }

    return {
        "notificationsEnabled": enabled,
        "roomTemperature": room_temperature,
        "windowOpenDuration": window_open_duration,
    }


def get_system_activations() -> dict[str, Any]:
    return {
        "activations": get_all(collections.systemActivation),
        "notificationsEnabled": notifications_enabled(),
    }


def get_user_activations(query: dict[str, Any]) -> dict[str, Any]:
    users = get_all(collections.managedUser)

    name = query.get("name")

    if name:
        needle = name.lower()
        users = [
            user
            for user in users
            if needle in f"{user.get('firstName')} {user.get('lastName')}".lower()
        ]

    roles = query.get("roles")

    if roles:
        role_list = roles.split(",")
        users = [user for user in users if user.get("role") in role_list]

    return paginate(users, query)


def create_rule(rule_type: str, body: RuleBody) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "active": body.active if body.active is not None else True,
        "createdAt": random_data.now_iso(),
        "id": random_data.next_id(),
        "scheduleTimeFrom": (
            body.scheduleTimeFrom if body.scheduleTimeFrom is not None else None
        ),
        "scheduleTimeTo": (
            body.scheduleTimeTo if body.scheduleTimeTo is not None else None
        ),
        "scheduleWeekdays": (
            body.scheduleWeekdays if body.scheduleWeekdays is not None else None
        ),
        "tags": body.tags if body.tags is not None else [],
        "threshold": body.threshold if body.threshold is not None else 0,
        "thresholdMinutes": (
            body.thresholdMinutes if body.thresholdMinutes is not None else 0
        ),
        "type": rule_type,
        "userId": body.userId if body.userId is not None else 0,
    }

    put(collections.rule, rule)

    return rule


def update_rule(id_: str, body: RuleBody) -> dict[str, Any]:
    updated_rule = patch(
        collections.rule, id_, body.model_dump(exclude_unset=True)
    )

    return updated_rule if updated_rule is not None else {"success": False}


def delete_rule(id_: str) -> dict[str, bool]:
    remove(collections.rule, id_)

    return {"success": True}


def update_system_activation(event_type: str, body: SystemActivationBody) -> dict[str, bool]:
    if "enabled" in body.model_fields_set:
        patch(collections.systemActivation, event_type, {"enabled": body.enabled})

    return {"success": True}


def update_user_activation(id_: str, body: NotificationsToggleBody) -> dict[str, bool]:
    if "notificationsEnabled" in body.model_fields_set:
        patch(
            collections.managedUser,
            id_,
            {"notificationsEnabled": body.notificationsEnabled},
        )

    return {"success": True}


def toggle_notifications(body: NotificationsToggleBody) -> dict[str, bool]:
    set_flag(
        "notificationsEnabled",
        body.notificationsEnabled if body.notificationsEnabled is not None else True,
    )

    return {"success": True}
