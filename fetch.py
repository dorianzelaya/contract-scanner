import httpx
import os
from dotenv import load_dotenv
from database import init_db, save_contract

load_dotenv()

API_KEY = os.getenv("SAM_API_KEY")

url = "https://api.sam.gov/opportunities/v2/search"

params = {
    "api_key": API_KEY,
    "postedFrom": "01/01/2025",
    "postedTo": "05/16/2025",
    "naicsCode": "238210",
    "limit": 5,
}

init_db()

response = httpx.get(url, params=params, timeout=30)
data = response.json()

contracts = data.get("opportunitiesData", [])

for contract in contracts:
    save_contract(contract)
    print(contract.get("title"))
    print(contract.get("responseDeadLine"))
    print(contract.get("uiLink"))
    print("---")