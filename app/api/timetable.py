from fastapi import APIRouter, Request
from app.db.connection import DbConfig
from app.db.repositories.timetable_view_repository import TimetableViewRepository

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


@router.get("/api/timetable/class/{class_id}")
def get_class_timetable(class_id: int, request: Request):
    repo = TimetableViewRepository(_db_cfg(request))
    return repo.get_by_class(class_id)
