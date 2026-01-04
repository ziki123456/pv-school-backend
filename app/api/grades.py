from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.db.connection import DbConfig
from app.db.repositories.grade_repository import GradeRepository

router = APIRouter()


class GradeCreateIn(BaseModel):
    student_id: int = Field(..., ge=1)
    subject_id: int = Field(..., ge=1)
    teacher_id: Optional[int] = Field(default=None, ge=1)
    value: float
    note: Optional[str] = None


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


@router.post("/api/grades")
def create_grade(payload: GradeCreateIn, request: Request):
    repo = GradeRepository(_db_cfg(request))
    try:
        new_id = repo.create_grade_and_touch_student(
            student_id=payload.student_id,
            subject_id=payload.subject_id,
            teacher_id=payload.teacher_id,
            value=payload.value,
            note=payload.note,
        )
        return {"ok": True, "id_grade": new_id, "created_at": datetime.utcnow().isoformat()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create grade: {e}")
