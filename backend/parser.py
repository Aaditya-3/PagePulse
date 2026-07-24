from typing import Any

from bs4 import BeautifulSoup

DEFAULT_TITLE = "No Title"
DEFAULT_META_DESCRIPTION = "No Description"


def parse_html(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    title = DEFAULT_TITLE
    if soup.title:
        title = soup.title.get_text(strip=True) or DEFAULT_TITLE

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = DEFAULT_META_DESCRIPTION
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"].strip() or DEFAULT_META_DESCRIPTION

    images_missing_alt = sum(
        1 for image in soup.find_all("img") if not image.get("alt")
    )
    word_count = len(soup.get_text(separator=" ", strip=True).split())

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_count": len(soup.find_all("h1")),
        "images_missing_alt": images_missing_alt,
        "word_count": word_count,
    }
