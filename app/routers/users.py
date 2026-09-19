from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user, pagination
from app.schemas.user import UserBody
from app.services import user_service

router = APIRouter()


@router.delete("/user/{user_id}")
def delete_user(user_id: str):
    return user_service.delete_user(user_id)


@router.get("/user/profile")
def get_profile(user: dict[str, Any] = Depends(get_current_user)):
    return user_service.get_profile(user)


@router.get("/user/list")
def get_users(
    query: dict[str, Any] = Depends(pagination),
    name: str | None = None,
    roles: str | None = None,
):
    return user_service.get_users({**query, "name": name, "roles": roles})


@router.post("/user")
def create_user(body: UserBody):
    user = user_service.create_user(body)

    return JSONResponse(status_code=201, content=user)


@router.put("/user/{user_id}")
def update_user(user_id: str, body: UserBody):
    return user_service.update_user(user_id, body)


@router.put("/user/{user_id}/reset-password")
def reset_password(user_id: str):
    return {"success": True}
