from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.heating import ProgramBody, ProgramCreateBody
from app.services import heating_service

router = APIRouter()


@router.get("/heatingschedule/list")
def get_programs():
    return heating_service.get_programs()


@router.get("/heatingschedule/{heating_schedule_id}/details")
def get_program_details(heating_schedule_id: str):
    return heating_service.get_program_details(heating_schedule_id)


@router.get("/heatingschedule/{heating_schedule_id}")
def get_program_by_id(heating_schedule_id: str):
    return heating_service.get_program_by_id(heating_schedule_id)


@router.post("/heatingschedule")
def create_program(body: ProgramCreateBody):
    program = heating_service.create_program(body.model_dump())

    return JSONResponse(status_code=201, content=program)


@router.post("/heatingschedule/{heating_schedule_id}/assignrooms")
def assign_rooms(heating_schedule_id: str):
    return {"success": True}


@router.put("/heatingschedule/{heating_schedule_id}")
def update_program_by_id(heating_schedule_id: str, body: ProgramBody):
    return heating_service.update_program_by_id(heating_schedule_id, body)


@router.delete("/heatingschedule/{heating_schedule_id}")
def delete_program_by_id(heating_schedule_id: str):
    return heating_service.delete_program_by_id(heating_schedule_id)
