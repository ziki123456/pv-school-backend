from fastapi import APIRouter, Request
from app.db.connection import DbConfig
from app.db.repositories.report_repository import ReportRepository

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


@router.get("/api/reports/class-subject-grades")
def report_class_subject_grades(request: Request):
    repo = ReportRepository(_db_cfg(request))
    return repo.get_class_subject_grades()
