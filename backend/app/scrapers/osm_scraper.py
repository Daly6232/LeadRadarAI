"""
OpenStreetMap / Overpass API scraper.
Free, no API key required.
"""
import requests
from typing import List, Dict


OVERPASS_URL = "https://overpass-api.de/api/interpreter"

OSM_CATEGORY_MAP = {
    "restaurant": ["amenity=restaurant", "amenity=cafe", "amenity=fast_food"],
    "dentist": ["amenity=dentist"],
    "doctor": ["amenity=doctors", "amenity=clinic"],
    "pharmacy": ["amenity=pharmacy"],
    "hotel": ["tourism=hotel", "tourism=guest_house"],
    "gym": ["leisure=fitness_centre", "leisure=sports_centre"],
    "school": ["amenity=school", "amenity=college"],
    "lawyer": ["office=lawyer", "office=legal"],
    "accountant": ["office=accountant"],
    "supermarket": ["shop=supermarket", "shop=grocery"],
    "bakery": ["shop=bakery"],
    "beauty": ["shop=beauty", "shop=hairdresser"],
    "bank": ["amenity=bank"],
    "garage": ["shop=car_repair", "amenity=car_rental"],
    "real_estate": ["office=estate_agent"],
}


def _build_query(filters: List[str], city: str, country: str, limit: int) -> str:
    area_query = f'area[name="{city}"][boundary=administrative]->.city;'
    node_queries = []
    for f in filters:
        key, val = f.split("=")
        node_queries.append(f'node[{key}="{val}"](area.city);')
        node_queries.append(f'way[{key}="{val}"](area.city);')
    union = "\n".join(node_queries)
    return f"""
[out:json][timeout:25];
{area_query}
(
{union}
);
out center {limit};
"""


def _parse_element(el: dict) -> Dict:
    tags = el.get("tags", {})
    lat = el.get("lat") or el.get("center", {}).get("lat")
    lon = el.get("lon") or el.get("center", {}).get("lon")

    phone = tags.get("phone") or tags.get("contact:phone") or tags.get("contact:mobile")
    email = tags.get("email") or tags.get("contact:email")
    website = tags.get("website") or tags.get("contact:website") or tags.get("url")
    name = tags.get("name") or tags.get("brand") or "Unknown Business"
    city = tags.get("addr:city") or tags.get("is_in:city", "")
    country = tags.get("addr:country", "")
    address_parts = [
        tags.get("addr:housenumber", ""),
        tags.get("addr:street", ""),
        city,
    ]
    address = " ".join(p for p in address_parts if p).strip()

    return {
        "business_name": name,
        "website": website,
        "email": email,
        "phone": phone,
        "city": city,
        "country": country,
        "address": address,
        "lat": lat,
        "lon": lon,
        "source": "openstreetmap",
    }


def scrape_businesses(category: str, city: str, country: str, limit: int = 20) -> List[Dict]:
    cat_key = category.lower().replace(" ", "_")
    filters = OSM_CATEGORY_MAP.get(cat_key, [f"name~\"{category}\""])

    query = _build_query(filters, city, country, limit)

    try:
        resp = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=30,
            headers={"User-Agent": "LeadRadarAI/1.0"}
        )
        resp.raise_for_status()
        data = resp.json()
        elements = data.get("elements", [])
        results = []
        seen = set()
        for el in elements:
            parsed = _parse_element(el)
            name = parsed["business_name"]
            if name != "Unknown Business" and name not in seen:
                seen.add(name)
                results.append(parsed)
        return results[:limit]
    except Exception as e:
        print(f"[OSM Scraper Error] {e}")
        return []
