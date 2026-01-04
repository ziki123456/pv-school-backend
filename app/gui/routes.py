from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/gui/templates")


@router.get("/", response_class=HTMLResponse)
def gui_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/timetable", response_class=HTMLResponse)
def gui_timetable(request: Request):
    return templates.TemplateResponse("timetable.html", {"request": request})
