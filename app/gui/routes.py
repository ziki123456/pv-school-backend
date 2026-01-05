from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.connection import DbConfig
from app.db.repositories.class_repository import ClassRepository
from app.db.repositories.timetable_view_repository import TimetableViewRepository
from app.db.repositories.report_repository import ReportRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/gui/templates")


# ⬇⬇⬇ Tohle už znáš – stejný styl jako v API
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


# -----------------------
# DASHBOARD
# -----------------------
@router.get("/", response_class=HTMLResponse)
def gui_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -----------------------
# ROZVRH TŘÍDY (DB VIEW)
# -----------------------
@router.get("/timetable", response_class=HTMLResponse)
def gui_timetable(request: Request, class_id: int | None = None):
    cfg = _db_cfg(request)

    # 1️⃣ načteme seznam tříd (dropdown)
    class_repo = ClassRepository(cfg)
    classes = class_repo.list_all()

    rows = []
    selected_class_id = None

    # 2️⃣ pokud je vybraná třída, načteme rozvrh z VIEW
    if class_id is not None:
        selected_class_id = int(class_id)
        tt_repo = TimetableViewRepository(cfg)
        rows = tt_repo.get_by_class(selected_class_id)

    # 3️⃣ pošleme data do šablony
    return templates.TemplateResponse(
        "timetable.html",
        {
            "request": request,
            "classes": classes,
            "selected_class_id": selected_class_id,
            "rows": rows,
        },
    )


@router.get("/reports", response_class=HTMLResponse)
def gui_reports(request: Request):
    cfg = _db_cfg(request)
    repo = ReportRepository(cfg)
    rows = repo.get_class_subject_grades()

    return templates.TemplateResponse(
        "report.html",
        {"request": request, "rows": rows},
    )
