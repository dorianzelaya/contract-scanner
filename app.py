from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, add_subscriber

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

@app.get("/", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Show the signup form."""
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup", response_class=HTMLResponse)
async def handle_signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    state: str = Form(...),
    naics_codes: str = Form(...),
    min_value: float = Form(0),
):
    """Handle signup form submission and save to database."""
    naics_list = [code.strip() for code in naics_codes.split(",")]
    add_subscriber(name, email, state if state else None, naics_list, min_value)
    return templates.TemplateResponse(request=request, name="success.html", context={"name": name})