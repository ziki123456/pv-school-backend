from fastapi import APIRouter, Request, HTTPException
import mysql.connector

from app.db.connection import DbConfig
from app.db.repositories.subject_repository import SubjectRepository
from app.db.repositories.teacher_subject_repository import TeacherSubjectRepository
from app.db.repositories.teacher_repository import TeacherRepository

router = APIRouter()


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


@router.get("/api/subjects")
def list_subjects(request: Request):
    repo = SubjectRepository(_db_cfg(request))
    return repo.list_all(active_only=True)


@router.get("/api/teachers/{teacher_id}/subjects")
def list_teacher_subjects(teacher_id: int, request: Request):
    cfg = _db_cfg(request)

    # verify teacher exists
    t_repo = TeacherRepository(cfg)
    if t_repo.get_by_id(int(teacher_id)) is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    ts_repo = TeacherSubjectRepository(cfg)
    rows = ts_repo.list_subjects_for_teacher(int(teacher_id))

    # return as list of dicts (simple, stable for JS)
    return [
        {
            "id_subject": int(r[0]),
            "name": r[1],
            "code": r[2],
            "subject_type": r[3],
            "is_active": bool(r[4]),
            "created_at": r[5].isoformat() if r[5] else None,
        }
        for r in rows
    ]


@router.post("/api/teachers/{teacher_id}/subjects/{subject_id}")
def assign_subject(teacher_id: int, subject_id: int, request: Request):
    cfg = _db_cfg(request)

    # verify teacher & subject exist
    t_repo = TeacherRepository(cfg)
    if t_repo.get_by_id(int(teacher_id)) is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    s_repo = SubjectRepository(cfg)
    if s_repo.get_by_id(int(subject_id)) is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    ts_repo = TeacherSubjectRepository(cfg)

    try:
        inserted = ts_repo.assign(int(teacher_id), int(subject_id))
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error")

    if not inserted:
        return {"assigned": False, "detail": "Assignment already exists"}

    return {"assigned": True, "teacher_id": int(teacher_id), "subject_id": int(subject_id)}


@router.delete("/api/teachers/{teacher_id}/subjects/{subject_id}")
def remove_subject(teacher_id: int, subject_id: int, request: Request):
    cfg = _db_cfg(request)

    ts_repo = TeacherSubjectRepository(cfg)
    try:
        removed = ts_repo.remove(int(teacher_id), int(subject_id))
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error")

    if not removed:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return {"removed": True, "teacher_id": int(teacher_id), "subject_id": int(subject_id)}
