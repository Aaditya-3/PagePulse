from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AuditRequest
from services import AuditError, fetch_page
from parser import parse_html

app = FastAPI(
    title="PagePulse API",
    version="1.0.0",
    description="Website auditing API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://pagepulse-4bgq.onrender.com",
 ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to PagePulse API"
    }


@app.post("/audit")
def audit_page(request: AuditRequest):
    try:
        response, response_time = fetch_page(request.url)
        report = parse_html(response.text)

        return {
            "status": response.status_code,
            "response_time_ms": response_time,
            **report
        }

    except AuditError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while auditing the website.",
        ) from e
