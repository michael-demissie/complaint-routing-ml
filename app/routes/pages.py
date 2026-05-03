from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "customer_portal.html")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.get("/customer-registration", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "customer_registration.html")

@router.get("/customer-dashboard", response_class=HTMLResponse)
def customer_dashboard(request: Request):
    return templates.TemplateResponse(request, "customer_dashboard.html")

@router.get("/complaint-submission", response_class=HTMLResponse)
def submit_page(request: Request):
    return templates.TemplateResponse(request, "complaint_submission.html")

@router.get("/operator-dashboard", response_class=HTMLResponse)
def operator_dashboard(request: Request):
    return templates.TemplateResponse(request, "operator_dashboard.html")

@router.get("/reviewer-dashboard", response_class=HTMLResponse)
def reviewer_dashboard(request: Request):
    return templates.TemplateResponse(request, "reviewer_dashboard.html")

@router.get("/staff-portal", response_class=HTMLResponse)
def staff_portal(request: Request):
    return templates.TemplateResponse(request, "staff_portal.html")

@router.get("/staff-registration", response_class=HTMLResponse)
def staff_register(request: Request):
    return templates.TemplateResponse(request, "staff_registration.html")
