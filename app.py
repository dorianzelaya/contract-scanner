from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, add_subscriber, get_conn
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

# Map trade categories to NAICS codes
TRADE_TO_NAICS = {
    "electrical": ["238210"],
    "plumbing_hvac": ["238220"],
    "general_construction": ["236220", "236210", "236110"],
    "roofing": ["238160"],
    "painting": ["238320"],
    "concrete_masonry": ["238110", "238140"],
    "site_work": ["238910", "237110", "237310"],
    "flooring": ["238330"],
    "drywall_insulation": ["238310"],
    "fire_protection": ["238290", "238210"],
    "landscaping": ["561730"],
    "janitorial": ["561720", "561210"],
}

@app.get("/", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Show the signup form."""
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup", response_class=HTMLResponse)
async def handle_signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    state: Optional[str] = Form(""),
    trades: List[str] = Form(...),
):
    """Handle signup form submission and save to database."""
    # Convert trade names to NAICS codes
    naics_codes = []
    for trade in trades:
        codes = TRADE_TO_NAICS.get(trade, [])
        naics_codes.extend(codes)
    # Remove duplicates
    naics_codes = list(set(naics_codes))

    add_subscriber(name, email, state if state else None, naics_codes, 0)
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