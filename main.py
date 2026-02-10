from fastapi import FastAPI
from database import init_db, get_connection
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "PoC is running with DB"}

@app.get("/deliberations")
def get_deliberations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM deliberations")
    rows = cursor.fetchall()

    conn.close()

    return {"data": rows}
@app.get("/insert-sample")
def insert_sample_endpoint():
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()

    # Δύο εγγραφές sample
    cursor.execute("""
    INSERT INTO deliberations
    (law_num, law_title, ministry, deliberation_title, deliberation_start, deliberation_end, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("1234", "Νόμος Δοκιμής", "Υπουργείο Παιδείας", "Συζήτηση για θέμα Χ", "2026-02-01", "2026-02-05", "manual", datetime.now().isoformat()))

    cursor.execute("""
    INSERT INTO deliberations
    (law_num, law_title, ministry, deliberation_title, deliberation_start, deliberation_end, source, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("5678", "Νόμος Δοκιμής 2", "Υπουργείο Οικονομικών", "Συζήτηση για θέμα Υ", "2026-01-15", "2026-01-20", "manual", datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return {"message": "Sample data inserted!"}
