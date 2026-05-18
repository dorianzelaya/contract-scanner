from filter import filter_contracts, subscriber
from summarize import summarize_contract

# Fake contracts to test our filter without hitting the API
fake_contracts = [
    {
        "noticeId": "abc123",
        "title": "Electrical work at LA Federal Building",
        "naicsCode": "238210",
        "officeAddress": {"state": "CA"},
        "responseDeadLine": "2026-06-01T17:00:00-05:00",
        "award": None,
        "uiLink": "https://sam.gov/fake1"
    },
    {
        "noticeId": "def456",
        "title": "Plumbing repair at Miami courthouse",
        "naicsCode": "238220",
        "officeAddress": {"state": "FL"},
        "responseDeadLine": "2026-06-15T17:00:00-05:00",
        "award": None,
        "uiLink": "https://sam.gov/fake2"
    },
    {
        "noticeId": "ghi789",
        "title": "IT support contract Virginia",
        "naicsCode": "541519",
        "officeAddress": {"state": "VA"},
        "responseDeadLine": "2026-06-10T17:00:00-05:00",
        "award": None,
        "uiLink": "https://sam.gov/fake3"
    },
]

matches = filter_contracts(fake_contracts, subscriber)

print(f"Found {len(matches)} matches:")

for contract in matches:
    summary = summarize_contract(contract)
    print(contract.get("title"))
    print(contract.get("uiLink"))
    print(summary)
    print("---")