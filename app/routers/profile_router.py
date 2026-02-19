from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router_profile = APIRouter()
templates = Jinja2Templates(directory="templates")

@router_profile.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request, "username": "Suji"})
