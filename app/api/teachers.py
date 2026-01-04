from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from app.db.connection import DbConfig
from app.db.repositories.teacher_repository import TeacherRepository
from app.core.models import TeacherCreate

router = APIRouter()


class TeacherCreateIn(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    hired_date: Optional[date] = None
    is_active: bool = True


def _db_cfg(request: Request) -> DbConfig:
    config = request.app.state.config
    db = config.db
    return DbConfig(
        host=db["host"],
        port=int(db["port"]),
        database=db["database"],
        user=db["user"],
        password=db["password"],
        charset=db.get("charset", "utf8mb4"),
    )


@router.post("/api/teachers")
def create_teacher(payload: TeacherCreateIn, request: Request):
    repo = TeacherRepository(_db_cfg(request))
    new_id = repo.create(
        TeacherCreate(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            email=str(payload.email) if payload.email else None,
            hired_date=payload.hired_date,
            is_active=payload.is_active,
        )
    )
    teacher = repo.get_by_id(new_id)
    if teacher is None:
        raise HTTPException(status_code=500, detail="Teacher insert failed")
    return teacher

@router.get("/api/teachers/{teacher_id}")
def get_teacher(teacher_id: int, request: Request):
    repo = TeacherRepository(_db_cfg(request))
    teacher = repo.get_by_id(teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.get("/api/teachers")
def list_teachers(
    request: Request,
    limit: int = 50,
    offset: int = 0,
):
    repo = TeacherRepository(_db_cfg(request))
    return repo.list_all(limit=limit, offset=offset)
