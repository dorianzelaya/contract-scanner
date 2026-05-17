import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("SAM_API_KEY")

# The SAM.gov endpoint we're hitting
url = "https://api.sam.gov/opportunities/v2/search"

# Filters for the API request
# naicsCode 238210 = electrical contractors
# limit 5 = only return 5 results at a time
params = {
    "api_key": API_KEY,
    "postedFrom": "01/01/2025",
    "postedTo": "05/16/2025",
    "naicsCode": "238210",
    "limit": 5,
}

# Create the database and contracts table if they don't exist yet
init_db()

# Hit the SAM.gov API and parse the JSON response
response = httpx.get(url, params=params, timeout=30)
data = response.json()

# Pull out the list of contracts from the response
# if the key doesn't exist, default to an empty list
contracts = data.get("opportunitiesData", [])

# Loop through each contract, save it to the database, and print the key info
for contract in contracts:
    save_contract(contract)
    print(contract.get("title"))
    print(contract.get("responseDeadLine"))
    print(contract.get("uiLink"))
    print("---")
    