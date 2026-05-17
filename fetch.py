import httpx
import os
from dotenv import load_dotenv

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

response = httpx.get(url, params=params, timeout=30)

print(response.status_code)
print(response.text)