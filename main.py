from fastapi import FastAPI
import sqlite3
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

DB_PATH = "data.db"

# -----------------------------
# Database helpers
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Πίνακας deliberations (από πριν)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliberations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        law_num TEXT,
        law_title TEXT,
        ministry TEXT,
        deliberation_title TEXT,
        deliberation_start TEXT,
        deliberation_end TEXT,
        source TEXT,
        last_updated TEXT
    )
    """)

    # Πίνακας laws (νομοσχέδια Βουλής)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        external_id TEXT UNIQUE,
        title TEXT,
        submission_date TEXT,
        ministry TEXT,
        source TEXT,
        last_synced TEXT
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# Startup
# -----------------------------
@app.on_event("startup")
def startup_event():
    init_db()

# -----------------------------
# Root / Health
# -----------------------------
@app.get("/")
def root():
    return {"message": "PoC is running with DB"}

@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Deliberations
# -----------------------------
@app.get("/deliberations")
def get_deliberations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deliberations")
    rows = cursor.fetchall()
    conn.close()
    return {"data": rows}

@app.get("/insert-sample")
def insert_sample():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO deliberations
    (law_num, law_title, ministry, deliberation_title,
     deliberation_start, deliberation_end, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "1234",
        "Νόμος Δοκιμής",
        "Υπουργείο Παιδείας",
        "Συζήτηση για θέμα Χ",
        "2026-02-01",
        "2026-02-05",
        "manual",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return {"message": "Sample deliberation inserted"}

# -----------------------------
# Laws – Sync from Parliament
# -----------------------------
@app.get("/sync/laws")
def sync_laws():
    url = "https://www.hellenicparliament.gr/OpenData/Laws"
    response = requests.get(url)

    root = ET.fromstring(response.content)

    conn = get_connection()
    cursor = conn.cursor()

    imported = 0

    for law in root.findall(".//Law"):
        external_id = law.findtext("Id")
        title = law.findtext("Title")
        submission_date = law.findtext("SubmissionDate")
        ministry = law.findtext("Ministry")

        cursor.execute("""
        INSERT OR IGNORE INTO laws
        (external_id, title, submission_date, ministry, source, last_synced)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            external_id,
            title,
            submission_date,
            ministry,
            "hellenic_parliament",
            datetime.now().isoformat()
        ))

        imported += 1

    conn.commit()
    conn.close()

    return {"imported": imported}

@app.get("/laws")
def get_laws():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laws")
    rows = cursor.fetchall()
    conn.close()
    return {"data": rows}

