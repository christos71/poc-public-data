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

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    return response.json()


