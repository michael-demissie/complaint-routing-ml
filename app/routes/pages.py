from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("customer_portal.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/customer-registration", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("customer_registration.html", {"request": request})

@router.get("/customer-dashboard", response_class=HTMLResponse)
def customer_dashboard(request: Request):
    return templates.TemplateResponse("customer_dashboard.html", {"request": request})

@router.get("/complaint-submission", response_class=HTMLResponse)
def submit_page(request: Request):
    return templates.TemplateResponse("complaint_submission.html", {"request": request})

@router.get("/operator-dashboard", response_class=HTMLResponse)
def operator_dashboard(request: Request):
    return templates.TemplateResponse("operator_dashboard.html", {"request": request})

@router.get("/reviewer-dashboard", response_class=HTMLResponse)
def reviewer_dashboard(request: Request):
    return templates.TemplateResponse("reviewer_dashboard.html", {"request": request})

@router.get("/staff-portal", response_class=HTMLResponse)
def staff_portal(request: Request):
    return templates.TemplateResponse("staff_portal.html", {"request": request})

@router.get("/staff-registration", response_class=HTMLResponse)
def staff_register(request: Request):
    return templates.TemplateResponse("staff_registration.html", {"request": request})
