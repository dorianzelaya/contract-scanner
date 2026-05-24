from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, add_subscriber, get_conn

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
):
    """Handle signup form submission and save to database."""
    naics_list = [code.strip() for code in naics_codes.split(",")]
    add_subscriber(name, email, state if state else None, naics_list, 0)
    return templates.TemplateResponse(request=request, name="success.html", context={"name": name})

@app.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(email: str = ""):
    """Deactivate a subscriber."""
    if email:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE subscribers SET active = 0 WHERE email = %s", (email,))
        conn.commit()
        conn.close()
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unsubscribed</title>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'DM Sans', sans-serif; background: #FAFAF8; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
            .card { background: #fff; border: 1px solid #e8e8e4; border-radius: 16px; padding: 60px 48px; text-align: center; max-width: 480px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); }
            h1 { font-family: 'DM Serif Display', serif; font-size: 24px; margin-bottom: 12px; }
            p { color: #666; font-size: 15px; line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>You've been unsubscribed</h1>
            <p>You won't receive any more contract alerts. If you change your mind, you can sign up again anytime.</p>
        </div>
    </body>
    </html>
    """)