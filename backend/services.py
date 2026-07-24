import requests
import time

def fetch_page(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    responseTime = (end - start) * 1000
    round(responseTime , 2)
    return response , responseTime
    
