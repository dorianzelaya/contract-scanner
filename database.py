import sqlite3

def init_db():
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            notice_id TEXT PRIMARY KEY,
            title TEXT,
            posted_date TEXT,
            deadline TEXT,
            naics_code TEXT,
            state TEXT,
            agency TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_contract(contract):
    conn = sqlite3.connect("contracts.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO contracts (notice_id, title, posted_date, deadline, naics_code, state, agency, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            contract.get("noticeId"),
            contract.get("title"),
            contract.get("postedDate"),
            contract.get("responseDeadLine"),
            contract.get("naicsCode"),
            contract.get("officeAddress", {}).get("state"),
            contract.get("fullParentPathName"),
            contract.get("uiLink"),
        )
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database created.")