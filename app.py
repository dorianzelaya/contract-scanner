from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, add_subscriber, get_conn
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

# Map trade categories to ALL relevant NAICS codes
TRADE_TO_NAICS = {
    "electrical": [
        "238210",  # Electrical contractors
        "237130",  # Power and communication line construction
    ],
    "plumbing_hvac": [
        "238220",  # Plumbing, heating, AC
        "238290",  # Other building equipment contractors
    ],
    "general_construction": [
        "236110",  # Residential building construction
        "236115",  # New single-family housing
        "236116",  # New multifamily housing
        "236117",  # New housing for-sale builders
        "236118",  # Residential remodelers
        "236210",  # Industrial building construction
        "236220",  # Commercial/institutional building construction
        "237990",  # Other heavy and civil engineering
        "238910",  # Site preparation contractors
        "238990",  # All other specialty trade contractors
    ],
    "roofing": [
        "238160",  # Roofing contractors
    ],
    "painting": [
        "238320",  # Painting and wall covering
    ],
    "concrete_masonry": [
        "238110",  # Poured concrete foundation and structure
        "238140",  # Masonry contractors
    ],
    "site_work": [
        "238910",  # Site preparation contractors
        "237110",  # Water and sewer line construction
        "237120",  # Oil and gas pipeline construction
        "237130",  # Power and communication line construction
        "237210",  # Land subdivision
        "237310",  # Highway, street, and bridge construction
        "237990",  # Other heavy and civil engineering
    ],
    "flooring": [
        "238330",  # Flooring contractors
        "238340",  # Tile and terrazzo contractors
    ],
    "drywall_insulation": [
        "238310",  # Drywall and insulation contractors
        "238350",  # Finish carpentry contractors
    ],
    "fire_protection": [
        "238290",  # Other building equipment contractors
        "238210",  # Electrical contractors (fire alarm systems)
        "238220",  # Plumbing (sprinkler systems)
    ],
    "landscaping": [
        "561730",  # Landscaping services
        "561790",  # Other services to buildings and dwellings
    ],
    "janitorial": [
        "561720",  # Janitorial services
        "561210",  # Facilities support services
        "561710",  # Exterminating and pest control
        "561790",  # Other services to buildings and dwellings
        "562111",  # Solid waste collection
        "562991",  # Septic tank and related services
        "811210",  # Electronic and precision equipment repair
    ],
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