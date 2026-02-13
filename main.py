from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="POC Laws API")

@app.get("/")
def root():
    return {"status": "poc is running"}

@app.get("/law/{lawnum}")
def get_law(lawnum: int):
    url = "https://www.hellenicparliament.gr/api.ashx"
    params = {
        "q": "laws",
        "lawnum": lawnum
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://www.hellenicparliament.gr/"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    return response.json()
