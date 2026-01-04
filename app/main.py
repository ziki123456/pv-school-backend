from fastapi import FastAPI
from pathlib import Path
from app.api.teachers import router as teachers_router
from app.api.grades import router as grades_router
from app.gui.routes import router as gui_router
from app.core.config import AppConfig
from app.api.db_ping import router as db_router
from app.api.db_tx_test import router as db_tx_router
from app.api.reports import router as reports_router
from app.api.timetable import router as timetable_router

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

config = AppConfig(CONFIG_PATH)

app = FastAPI(title="PV School App")
app.state.config = config


app.include_router(db_router)
app.include_router(db_tx_router)
app.include_router(teachers_router)
app.include_router(grades_router)
app.include_router(reports_router)
app.include_router(timetable_router)
app.include_router(gui_router)



@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "db": config.db["database"],
    }
