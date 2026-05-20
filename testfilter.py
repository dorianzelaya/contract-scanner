from filter import filter_contracts, subscriber
from summarize import summarize_contract
from emailsender import send_digest

# Fake contracts to test the full pipeline
fake_contracts = [
    {
        "noticeId": "abc123",
        "title": "Electrical work at Miami Federal Building",
        "naicsCode": "238210",
        "officeAddress": {"state": "DC"},
        "placeOfPerformance": {"state": {"code": "FL"}},
        "responseDeadLine": "2026-06-01T17:00:00-05:00",
        "fullParentPathName": "DEPT OF HOMELAND SECURITY.FEDERAL PROTECTIVE SERVICE",
        "award": None,
        "uiLink": "https://sam.gov/fake1",
        "description": "https://api.sam.gov/fake"
    },
    {
        "noticeId": "def456",
        "title": "IT support contract Virginia",
        "naicsCode": "541519",
        "officeAddress": {"state": "VA"},
        "placeOfPerformance": {"state": {"code": "VA"}},
        "responseDeadLine": "2026-06-10T17:00:00-05:00",
        "fullParentPathName": "DEPT OF DEFENSE",
        "award": None,
        "uiLink": "https://sam.gov/fake2",
        "description": "https://api.sam.gov/fake2"
    },
]

# Filter contracts
matches = filter_contracts(fake_contracts, subscriber)

# Summarize each match
summaries = []
for contract in matches:
    summary = summarize_contract(contract)
    summaries.append(summary)

# Send the email
send_digest(subscriber, matches, summaries)