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
