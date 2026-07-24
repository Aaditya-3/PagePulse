import time
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


def fetch_page(url: str):
    try:
        start = time.perf_counter()

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        response_time = round(
            (time.perf_counter() - start) * 1000,
            2
        )

        return response, response_time

    except requests.exceptions.Timeout:
        raise Exception("The request timed out.")

    except requests.exceptions.ConnectionError:
        raise Exception("Unable to connect to the website.")

    except requests.exceptions.InvalidURL:
        raise Exception("Invalid URL.")

    except requests.exceptions.MissingSchema:
        raise Exception("URL must start with http:// or https://")

    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Website returned HTTP {e.response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        raise Exception(str(e))