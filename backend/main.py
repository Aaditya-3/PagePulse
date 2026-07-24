from fastapi import FastAPI
from models import AuditRequest
from services import fetch_page
from parser import parse_html

app = FastAPI()
@app.get('/')
def hello():
    return "hello"

@app.post('/audit')
def post_url(request : AuditRequest):
   response , responseTime = fetch_page(request.url)
   report = parse_html(response.text)
   return{
       "status" : response.status_code,
       "response_time_ms" : responseTime,
       **report
   }
