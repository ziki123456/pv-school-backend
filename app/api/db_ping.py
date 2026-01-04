from fastapi import APIRouter, Request

from app.db.connection import DbConfig, ping_db

router = APIRouter()


@router.get("/api/db/ping")
def db_ping(request: Request):
    config = request.app.state.config
    db = config.db

    cfg = DbConfig(
        host=db["host"],
        port=int(db["port"]),
        database=db["database"],
        user=db["user"],
        password=db["password"],
        charset=db.get("charset", "utf8mb4"),
    )
    return ping_db(cfg)
