import re
import time
from dataclasses import dataclass
from typing import Final
from urllib.parse import urlparse, urlunparse

import requests

REQUEST_TIMEOUT_SECONDS: Final[int] = 10
DEFAULT_SCHEME: Final[str] = "https"
DEFAULT_TLD: Final[str] = ".com"
HTML_CONTENT_TYPES: Final[tuple[str, ...]] = ("text/html", "application/xhtml+xml")

HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

HOSTNAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


@dataclass
class AuditError(Exception):
    message: str
    status_code: int = 400

    def __str__(self) -> str:
        return self.message

def normalize_url(url: str) -> str:
    url = url.strip()

    if not url:
        raise AuditError("Please enter a URL.")

    if not url.startswith(("http://", "https://")):
        if "." not in url:
            url += ".com"

        url = "https://" + url

    return url

def is_html_response(response: requests.Response) -> bool:
    content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    return content_type.lower() in HTML_CONTENT_TYPES


def fetch_page(url: str) -> tuple[requests.Response, float]:
    normalized_url = normalize_url(url)
    start = time.perf_counter()

    try:
        response = requests.get(
            normalized_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )

        response.raise_for_status()

        if not is_html_response(response):
            raise AuditError("The URL did not return an HTML page.", status_code=415)

        response_time = round((time.perf_counter() - start) * 1000, 2)
        return response, response_time

    except requests.exceptions.SSLError:
     raise AuditError(
        "The website has an invalid SSL certificate.",
        status_code=400
    )

    except requests.exceptions.InvalidURL:
     raise AuditError(
        "Invalid URL.",
        status_code=400
    )

    except requests.exceptions.MissingSchema:
     raise AuditError(
        "Please enter a valid website URL.",
        status_code=400
    )

    except requests.exceptions.SSLError as e:
     raise AuditError(
        f"SSL Error: {e}",
        status_code=502
    )

    except requests.exceptions.ConnectionError:
     raise AuditError(
        "Invalid or unreachable URL.",
        status_code=400
    )

    except requests.exceptions.TooManyRedirects:
      raise AuditError(
        "The website redirected too many times.",
        status_code=400
    )

    except requests.exceptions.HTTPError as e:
     code = e.response.status_code

     if code == 404:
        raise AuditError("Website not found.", status_code=404)

     elif code == 403:
        raise AuditError("Access to the website was denied.", status_code=403)

     elif code >= 500:
        raise AuditError("The website is currently unavailable.", status_code=502)

     else:
        raise AuditError(
            f"Website returned HTTP {code}.",
            status_code=400
        )

    except requests.exceptions.RequestException:
     raise AuditError(
        "Unable to fetch the website.",
        status_code=500
    )