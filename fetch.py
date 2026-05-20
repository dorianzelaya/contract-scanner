import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract
from filter import filter_contracts, subscriber
from summarize import summarize_contract
from emailsender import send_digest

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("SAM_API_KEY")

# The SAM.gov endpoint we're hitting
url = "https://api.sam.gov/opportunities/v2/search"

# Filters for the API request
params = {
    "api_key": API_KEY,
    "postedFrom": "02/01/2026",
    "postedTo": "05/19/2026",
    "limit": 1000,
}

# Create the database and contracts table if they don't exist yet
init_db()

# Hit the SAM.gov API and parse the JSON response
response = httpx.get(url, params=params, timeout=30)
data = response.json()

# Pull out the list of contracts from the response
contracts = data.get("opportunitiesData", [])

# Filter contracts down to only the ones matching the subscriber's profile
matches = filter_contracts(contracts, subscriber)

# Summarize top 5 matches and collect summaries
summaries = []
for contract in matches[:5]:
    save_contract(contract)
    summary = summarize_contract(contract)
    summaries.append(summary)
    print(contract.get("title"))
    print(contract.get("responseDeadLine"))
    print(contract.get("uiLink"))
    print(summary)
    print("---")

# Send the digest email
send_digest(subscriber, matches[:5], summaries)

print(f"Found {len(matches)} matching contracts out of {len(contracts)} total.")