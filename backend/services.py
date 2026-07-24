import requests
import time

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

def fetch_page(url):
  
    start = time.perf_counter()

    response = requests.get(url , headers = headers , timeout = 10)
    end = time.time()

    response_time = round((time.perf_counter() - start) * 1000 , 2)
    return response , response_time
    
