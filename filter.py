# A subscriber profile — this represents one contractor's preferences
# Later this will come from the database, but for now it's hardcoded for testing
subscriber = {
    "name": "Test Subscriber",
    "email": "dorianjzelaya@gmail.com",
    "naics_codes": ["238210", "238220", "238290", "237990", "236220"],
    "state": None,
    "min_value": 0,
}

def filter_contracts(contracts, subscriber):
    """Filter a list of contracts down to only the ones matching a subscriber's profile."""
    matches = []

    for contract in contracts:
        naics = contract.get("naicsCode", "")
        pop = contract.get("placeOfPerformance") or {}
        state = pop.get("state", {})
        if isinstance(state, dict):
            state = state.get("code", "")
        if not state:
            state = (contract.get("officeAddress") or {}).get("state", "")
        award = contract.get("award", {}) or {}
        value = float(award.get("amount", 0) or 0)

        # check if the contract matches the subscriber's filters
        naics_match = naics in subscriber["naics_codes"]
        state_match = True if not subscriber["state"] else state == subscriber["state"]
        value_match = value >= subscriber["min_value"] or value == 0

        if naics_match and state_match and value_match:
            matches.append(contract)

    return matches