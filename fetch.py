import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract, get_subscribers
from filter import filter_contracts
from summarize import summarize_contract
from emailsender import send_digest
from datetime import date

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
subscribers = get_subscribers()
print(f"Sending to {len(subscribers)} subscribers")

# For each subscriber, filter, summarize, and send their personalized email
for subscriber in subscribers:
    matches = filter_contracts(contracts, subscriber)
    
    summaries = []
    for contract in matches[:5]:
        save_contract(contract)
        summary = summarize_contract(contract)
        summaries.append(summary)

    send_digest(subscriber, matches[:5], summaries)
    print(f"Sent {len(matches[:5])} contracts to {subscriber['email']}")