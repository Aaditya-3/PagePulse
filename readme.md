# Page Pulse

Page Pulse is a FastAPI + React website audit console built for the Digital
Heroes training task.

The backend accepts incomplete URLs such as `google`, `google.com`, and
`www.google.com`, normalizes them, fetches the page, and returns a simple audit
report.

## Backend

```bash
cd PagePulse/backend
..\..\myenv\Scripts\python.exe -m uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

`POST /audit`

```json
{
  "url": "google"
}
```

Returns:

```json
{
  "status": 200,
  "response_time_ms": 452.31,
  "title": "Google",
  "meta_description": "No Description",
  "h1_count": 0,
  "images_missing_alt": 6,
  "word_count": 72
}
```

## Frontend

```bash
cd PagePulse/frontend
npm.cmd install
npm.cmd run dev
```

The React app runs at `http://127.0.0.1:5173` and proxies `/api` requests to
the backend.
