from fastapi import FastAPI
from pathlib import Path

from app.core.config import AppConfig

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

config = AppConfig(CONFIG_PATH)

app = FastAPI(title="PV School App")


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "app_host": config.app["host"],
        "db_host": config.db["host"],
    }
