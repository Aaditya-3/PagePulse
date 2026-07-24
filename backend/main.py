from fastapi import FastAPI, HTTPException

from models import AuditRequest
from services import fetch_page
from parser import parse_html

app = FastAPI(
    title="PagePulse API",
    version="1.0.0",
    description="Website auditing API"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to PagePulse API"
    }


@app.post("/audit")
def audit_page(request: AuditRequest):
    try:
        response, response_time = fetch_page(str(request.url))

        report = parse_html(response.text)

        return {
            "status": response.status_code,
            "response_time_ms": response_time,
            **report
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )