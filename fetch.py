import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract
from filter import filter_contracts, subscriber

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("SAM_API_KEY")

# The SAM.gov endpoint we're hitting
url = "https://api.sam.gov/opportunities/v2/search"

# Filters for the API request
params = {
    "api_key": API_KEY,
    "postedFrom": "01/01/2026",
    "postedTo": "05/17/2026",
    "naicsCode": "238210,238220",
    "limit": 100,
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

# Loop through matched contracts, save to database, and print key info
for contract in matches:
    save_contract(contract)
    print(contract.get("title"))
    print(contract.get("responseDeadLine"))
    print(contract.get("uiLink"))
    print("---")

print(f"Found {len(matches)} matching contracts out of {len(contracts)} total.")