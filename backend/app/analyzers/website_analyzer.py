"""
Website analyzer — checks existence, HTTPS, pages, meta tags, contacts, social links.
Termux-compatible: uses only requests + BeautifulSoup.
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict
from urllib.parse import urljoin, urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; Mobile) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Mobile Safari/537.36"
    )
}
TIMEOUT = 10

SOCIAL_PATTERNS = {
    "facebook": r"facebook\.com/(?!sharer|share|login|home|photo|video|pages/create)",
    "instagram": r"instagram\.com/",
    "linkedin": r"linkedin\.com/(?:company|in)/",
    "twitter": r"(?:twitter|x)\.com/",
    "tiktok": r"tiktok\.com/@",
    "youtube": r"youtube\.com/(?:c/|channel/|@|user/)",
}

PAGE_KEYWORDS = {
    "contact": ["contact", "contacts", "contactez", "kontakt", "اتصل"],
    "about": ["about", "about-us", "a-propos", "qui-sommes", "من نحن"],
    "services": ["services", "service", "prestations", "خدمات"],
}


def _get_page(url: str) -> tuple:
    """Returns (response, soup, final_url) or (None, None, url)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        soup = BeautifulSoup(resp.text, "html.parser")
        return resp, soup, resp.url
    except Exception:
        return None, None, url


def _normalize_url(website: str) -> str:
    if not website:
        return ""
    if not website.startswith("http"):
        website = "https://" + website
    return website.rstrip("/")


def _extract_emails(text: str) -> str:
    emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    filtered = [e for e in emails if not any(x in e for x in ["example", "test", "domain", "email@"])]
    return filtered[0] if filtered else None


def _extract_phones(text: str) -> str:
    phones = re.findall(r"[\+\(]?[\d\s\-\(\)]{7,20}", text)
    cleaned = ["".join(re.findall(r"[\d\+]", p)) for p in phones]
    valid = [p for p in cleaned if 7 <= len(p) <= 15]
    return valid[0] if valid else None


def _extract_social(text: str) -> Dict[str, str]:
    found = {}
    for platform, pattern in SOCIAL_PATTERNS.items():
        match = re.search(r'https?://(?:www\.)?' + pattern + r'[^\s\'"<>]+', text, re.IGNORECASE)
        if match:
            found[platform] = match.group(0).rstrip("/")
    return found


def _check_subpages(base_url: str, links: list) -> Dict[str, bool]:
    result = {"has_contact_page": False, "has_about_page": False, "has_services_page": False}
    hrefs = []
    for link in links:
        href = link.get("href", "")
        if href:
            hrefs.append(href.lower())

    for page_type, keywords in PAGE_KEYWORDS.items():
        key = f"has_{page_type}_page"
        for href in hrefs:
            if any(kw in href for kw in keywords):
                result[key] = True
                break
    return result


def analyze_website(website: str) -> Dict:
    result = {
        "has_website": False,
        "https_enabled": False,
        "has_contact_page": False,
        "has_about_page": False,
        "has_services_page": False,
        "meta_title": None,
        "meta_description": None,
        "email": None,
        "phone": None,
        "facebook": None,
        "instagram": None,
        "linkedin": None,
        "twitter": None,
        "tiktok": None,
        "youtube": None,
    }

    url = _normalize_url(website)
    if not url:
        return result

    resp, soup, final_url = _get_page(url)
    if resp is None or resp.status_code >= 400:
        # Try http fallback
        if url.startswith("https://"):
            resp, soup, final_url = _get_page(url.replace("https://", "http://"))
        if resp is None:
            return result

    result["has_website"] = True
    result["https_enabled"] = final_url.startswith("https://")

    # Meta
    title_tag = soup.find("title")
    if title_tag:
        result["meta_title"] = title_tag.text.strip()[:200]

    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        result["meta_description"] = desc_tag.get("content", "")[:300]

    # All links
    links = soup.find_all("a", href=True)
    page_check = _check_subpages(final_url, links)
    result.update(page_check)

    # Full text for extraction
    full_text = soup.get_text(" ") + " " + resp.text

    # Emails & phones
    extracted_email = _extract_emails(full_text)
    if extracted_email:
        result["email"] = extracted_email

    extracted_phone = _extract_phones(full_text)
    if extracted_phone:
        result["phone"] = extracted_phone

    # Social links
    social = _extract_social(resp.text)
    result.update(social)

    return result
