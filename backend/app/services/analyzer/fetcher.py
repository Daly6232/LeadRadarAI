import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "LeadRadarAI/1.0"
}


def fetch_website(url: str):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    return {
        "status": response.status_code,
        "html": response.text,
        "soup": soup,
        "headers": dict(response.headers),
    }
