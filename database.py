import sqlite3

def init_db():
    # Connect to the database file, creates it if it doesn't exist yet
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()

    # Create the contracts table if it doesn't already exist
    # notice_id is the PRIMARY KEY — meaning no two rows can have the same one
    # this is what prevents duplicate contracts from being saved
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            notice_id TEXT PRIMARY KEY,
            title TEXT,
            posted_date TEXT,
            deadline TEXT,
            naics_code TEXT,
            state TEXT,
            agency TEXT,
            url TEXT,
            set_aside TEXT,
            description_url TEXT,
            award_amount TEXT,
            place_of_performance TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            state TEXT,
            naics_codes TEXT,
            min_value REAL,
            active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

def save_contract(contract):
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()

    # INSERT OR IGNORE means: if a contract with this notice_id already exists,
    # skip it silently. if it's new, insert it. this is the deduplication.
    # the ? placeholders are filled in by the tuple below — this prevents SQL injection
    cursor.execute(
        "INSERT OR IGNORE INTO contracts (notice_id, title, posted_date, deadline, naics_code, state, agency, url, set_aside, description_url, award_amount, place_of_performance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            contract.get("noticeId"),
            contract.get("title"),
            contract.get("postedDate"),
            contract.get("responseDeadLine"),
            contract.get("naicsCode"),
            contract.get("officeAddress", {}).get("state"),
            contract.get("fullParentPathName"),
            contract.get("uiLink"),
            contract.get("typeOfSetAsideDescription"),
            contract.get("description"),
            contract.get("award", {}).get("amount") if contract.get("award") else None,
            contract.get("placeOfPerformance", {}).get("zip") if contract.get("placeOfPerformance") else None,
        )
    )

    conn.commit()
    conn.close()
    
def add_subscriber(name, email, state, naics_codes, min_value=0):
    """Add a new subscriber to the database."""
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO subscribers (name, email, state, naics_codes, min_value) VALUES (?, ?, ?, ?, ?)",
        (name, email, state, ",".join(naics_codes), min_value)
    )
    conn.commit()
    conn.close()

def get_subscribers():
    """Get all active subscribers from the database."""
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, state, naics_codes, min_value FROM subscribers WHERE active = 1")
    rows = cursor.fetchall()
    conn.close()
    subscribers = []
    for row in rows:
        subscribers.append({
            "name": row[0],
            "email": row[1],
            "state": row[2] if row[2] else None,
            "naics_codes": row[3].split(","),
            "min_value": row[4],
        })
    return subscribers

# this block only runs if you execute database.py directly
# it won't run when fetch.py imports from it
if __name__ == "__main__":
    init_db()
    print("Database created.")