import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract, get_subscribers, get_conn
from filter import filter_contracts
from summarize import summarize_contract
from emailsender import send_digest
from datetime import date, datetime, timedelta

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("SAM_API_KEY")

# The SAM.gov endpoint we're hitting
url = "https://api.sam.gov/opportunities/v2/search"

# Filters for the API request
params = {
    "api_key": API_KEY,
    "postedFrom": "02/01/2026",
    "postedTo": date.today().strftime("%m/%d/%Y"),
    "limit": 1000,
}

# Create the database and tables if they don't exist yet
init_db()

# Hit the SAM.gov API and parse the JSON response
response = httpx.get(url, params=params, timeout=30)
data = response.json()

# Pull out the list of contracts from the response
contracts = data.get("opportunitiesData", [])

print(f"Pulled {len(contracts)} contracts from SAM.gov")

# Get all active subscribers from the database
conn = get_conn()
cursor = conn.cursor()
cursor.execute("SELECT name, email, state, naics_codes, min_value, signup_date FROM subscribers WHERE active = 1")
rows = cursor.fetchall()
conn.close()

print(f"Found {len(rows)} active subscribers")

def deadline_sort_key(contract):
    """Sort contracts by deadline — soonest first, no deadline last."""
    deadline = contract.get("responseDeadLine")
    if not deadline:
        return datetime.max
    try:
        return datetime.fromisoformat(deadline)
    except:
        return datetime.max

for row in rows:
    subscriber = {
        "name": row[0],
        "email": row[1],
        "state": row[2] if row[2] else None,
        "naics_codes": row[3].split(","),
        "min_value": row[4],
    }
    signup_date = row[5]

    # Check if free trial has expired (14 days)
    if signup_date:
        days_active = (datetime.now() - signup_date).days
        if days_active > 14:
            print(f"Trial expired for {subscriber['email']} ({days_active} days). Skipping.")
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("UPDATE subscribers SET active = 0 WHERE email = %s", (subscriber['email'],))
            conn.commit()
            conn.close()
            continue

    matches = filter_contracts(contracts, subscriber)

    # Sort by deadline — soonest first
    matches.sort(key=deadline_sort_key)

    # Take top 10 contracts
    top_matches = matches[:10]

    summaries = []
    for contract in top_matches:
        save_contract(contract)
        summary = summarize_contract(contract)
        summaries.append(summary)

    send_digest(subscriber, top_matches, summaries)
    print(f"Sent {len(top_matches)} contracts to {subscriber['email']}")