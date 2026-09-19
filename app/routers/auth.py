from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.auth import LoginBody, RegisterBody
from app.services import auth_service

router = APIRouter()


@router.post("/auth/login")
def login(body: LoginBody):
    return auth_service.login(body.email, body.password)


@router.post("/auth/register")
def register(body: RegisterBody):
    result = auth_service.register(
        body.email, body.firstName, body.lastName, body.password, body.role
    )

    return JSONResponse(status_code=201, content=result)
