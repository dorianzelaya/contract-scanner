import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    """Connect to PostgreSQL database."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    conn = get_conn()
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
            url TEXT,
            set_aside TEXT,
            description_url TEXT,
            award_amount TEXT,
            place_of_performance TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            state TEXT,
            naics_codes TEXT,
            min_value REAL DEFAULT 0,
            active INTEGER DEFAULT 1,
            signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_contract(contract):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO contracts (notice_id, title, posted_date, deadline, naics_code, state, agency, url, set_aside, description_url, award_amount, place_of_performance) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (notice_id) DO NOTHING""",
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
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO subscribers (name, email, state, naics_codes, min_value) 
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING""",
        (name, email, state, ",".join(naics_codes), min_value)
    )
    conn.commit()
    conn.close()

def get_subscribers():
    """Get all active subscribers from the database."""
    conn = get_conn()
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

if __name__ == "__main__":
    init_db()
    print("Database created.")