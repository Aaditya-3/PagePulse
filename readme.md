# PagePulse

PagePulse is a lightweight website auditing tool built using **React** and **FastAPI**. It allows users to enter a website URL and receive a quick audit containing useful SEO and webpage metrics.

## Features

- Website Title
- Meta Description
- HTTP Status Code
- Response Time
- H1 Count
- Word Count
- Images Missing Alt Attributes
- User-friendly error handling
- Responsive frontend
- Live deployment

---

## Tech Stack

### Frontend

- React
- Vite

### Backend

- FastAPI
- Requests
- BeautifulSoup4

---

## Project Structure

```
PagePulse
│
├── backend
│   ├── main.py
│   ├── parser.py
│   ├── services.py
│   ├── models.py
│   ├── test_parser.py
│   └── requirements.txt
│
└── frontend
```

---

## Installation

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Runs on

```
http://localhost:8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Runs on

```
http://localhost:5173
```

---

## API Contract

### POST /audit

### Request

```json
{
    "url":"google.com"
}
```

### Successful Response

```json
{
    "status":200,
    "response_time_ms":121,
    "title":"Google",
    "meta_description":"Search Engine",
    "h1_count":1,
    "images_missing_alt":2,
    "word_count":537
}
```

---

## Running Tests

```bash
cd backend

pytest
```

The tests cover:

- Happy path parsing
- Missing title
- Missing meta description

---

## Design Decisions

### 1. Separation of Concerns

Fetching webpage content and parsing HTML are implemented in different modules (`services.py` and `parser.py`). This makes the project easier to maintain and test.

---

### 2. BeautifulSoup for HTML Parsing

BeautifulSoup provides a simple and reliable way to parse HTML documents and extract structured information such as titles, headings and meta tags.

---

### 3. FastAPI for Backend

FastAPI was chosen because it provides automatic request validation using Pydantic, built-in API documentation through Swagger UI, and a clean structure for REST APIs.

---

## Future Improvements

If given more time I would:

- Add asynchronous HTTP requests using `httpx`
- Cache repeated requests
- Add robots.txt and sitemap analysis
- Improve SEO metrics
- Add Lighthouse-style performance checks
- Expand unit test coverage

---

## Live Demo

Frontend

https://pagepulse-4bgq.onrender.com

Backend

https://pagepulse-api.onrender.com

---

Built for **Digital Heroes Training Task**