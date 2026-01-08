from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
import mysql.connector

from app.db.connection import DbConfig
from app.db.repositories.student_repository import StudentRepository
from app.core.models import StudentCreate

router = APIRouter()


class StudentCreateIn(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    class_id: Optional[int] = None
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


@router.post("/api/students")
def create_student(payload: StudentCreateIn, request: Request):
    repo = StudentRepository(_db_cfg(request))
    new_id = repo.create(
        StudentCreate(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            birth_date=payload.birth_date,
            class_id=payload.class_id,
            is_active=payload.is_active,
        )
    )
    student = repo.get_by_id(new_id)
    if student is None:
        raise HTTPException(status_code=500, detail="Student insert failed")
    return student


@router.get("/api/students")
def list_students(request: Request, limit: int = 50, offset: int = 0):
    repo = StudentRepository(_db_cfg(request))
    return repo.list_all(limit=limit, offset=offset)


@router.get("/api/students/{student_id}")
def get_student(student_id: int, request: Request):
    repo = StudentRepository(_db_cfg(request))
    student = repo.get_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/api/students/{student_id}")
def update_student(student_id: int, payload: StudentCreateIn, request: Request):
    repo = StudentRepository(_db_cfg(request))

    existing = repo.get_by_id(student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")

    ok = repo.update(
        student_id,
        StudentCreate(
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            birth_date=payload.birth_date,
            class_id=payload.class_id,
            is_active=payload.is_active,
        ),
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")

    student = repo.get_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=500, detail="Student update failed")
    return student


@router.delete("/api/students/{student_id}")
def delete_student(student_id: int, request: Request):
    repo = StudentRepository(_db_cfg(request))

    try:
        deleted = repo.delete(student_id)
    except mysql.connector.Error as e:
        # FK constraint (e.g., student referenced in grade)
        if getattr(e, "errno", None) in (1451, 1452):
            raise HTTPException(
                status_code=409,
                detail="Cannot delete student because it is referenced by other records",
            )
        raise HTTPException(status_code=500, detail="Database error")

    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"deleted": True, "id_student": student_id}
