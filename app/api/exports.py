import csv
import io
from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.db.connection import DbConfig
from app.db.repositories.export_repository import ExportRepository

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


@router.get("/api/export/teachers.csv")
def export_teachers_csv(request: Request):
    repo = ExportRepository(_db_cfg(request))
    rows = repo.list_teachers()

    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id_teacher", "first_name", "last_name", "email", "hired_date", "is_active", "created_at"])
    for r in rows:
        w.writerow(list(r))

    return Response(
        content=buf.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=teachers.csv"},
    )


@router.get("/api/export/students.csv")
def export_students_csv(request: Request):
    repo = ExportRepository(_db_cfg(request))
    rows = repo.list_students()

    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id_student", "first_name", "last_name", "birth_date", "class_id", "is_active", "created_at", "last_grade_at"])
    for r in rows:
        w.writerow(list(r))

    return Response(
        content=buf.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=students.csv"},
    )
