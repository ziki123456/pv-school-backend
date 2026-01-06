from fastapi import APIRouter, Request, HTTPException
from pathlib import Path

from app.db.connection import DbConfig
from app.db.repositories.import_repository import ImportRepository

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
IMPORT_DIR = BASE_DIR / "db" / "import"


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


@router.post("/api/import/teachers")
def import_teachers(request: Request):
    csv_path = IMPORT_DIR / "teachers.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="teachers.csv not found in db/import")

    repo = ImportRepository(_db_cfg(request))
    try:
        rows = repo.load_teachers_csv(csv_path)
        return repo.import_teachers(rows)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/import/students")
def import_students(request: Request):
    csv_path = IMPORT_DIR / "students.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="students.csv not found in db/import")

    repo = ImportRepository(_db_cfg(request))
    try:
        rows = repo.load_students_csv(csv_path)
        return repo.import_students(rows)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
