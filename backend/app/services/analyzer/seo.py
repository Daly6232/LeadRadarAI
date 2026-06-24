from bs4 import BeautifulSoup


def analyze_seo(soup: BeautifulSoup):
    title = soup.title.string.strip() if soup.title and soup.title.string else None

    description = None
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        description = meta.get("content")

    h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]

    og_title = None
    og = soup.find("meta", attrs={"property": "og:title"})
    if og:
        og_title = og.get("content")

    return {
        "title": title,
        "meta_description": description,
        "h1_count": len(h1_tags),
        "h1_tags": h1_tags,
        "og_title": og_title,
    }
