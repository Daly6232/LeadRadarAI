import requests
import time


class OSMScraper:
    """
    Stable OSM scraper with automatic Overpass fallback.
    """

    def __init__(self):

        self.overpass_urls = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://lz4.overpass-api.de/api/interpreter"
        ]

        self.headers = {
            "User-Agent": "LeadRadarAI/1.0",
            "Accept": "*/*"
        }

        self.bboxes = {
            "Tunis": (36.74, 10.14, 36.88, 10.25),
            "Sfax": (34.71, 10.69, 34.80, 10.78),
            "Sousse": (35.80, 10.60, 35.88, 10.66),
        }

    def _query_overpass(self, query):

        last_error = None

        for url in self.overpass_urls:

            for attempt in range(2):

                try:
                    response = requests.post(
                        url,
                        data=query,
                        headers=self.headers,
                        timeout=30
                    )

                    response.raise_for_status()

                    return response.json()

                except Exception as e:
                    last_error = e
                    time.sleep(1)

        raise Exception(last_error)

    def search(self, category: str, city: str, limit: int = 10):

        if city not in self.bboxes:
            return {
                "error": f"City '{city}' not supported yet",
                "strong": [],
                "weak": []
            }

        south, west, north, east = self.bboxes[city]

        query = f"""
[out:json][timeout:25];
(
  node["amenity"="{category}"]({south},{west},{north},{east});
  way["amenity"="{category}"]({south},{west},{north},{east});
  relation["amenity"="{category}"]({south},{west},{north},{east});
);
out center;
"""

        try:

            data = self._query_overpass(query)

            strong = []
            weak = []

            seen = set()

            for el in data.get("elements", []):

                tags = el.get("tags", {})

                name = tags.get("name")

                if not name:
                    continue

                if name in seen:
                    continue

                seen.add(name)

                business = {
    "name": name,
    "category": tags.get("amenity"),
    "city": city,

    # location
    "lat": el.get("lat") or el.get("center", {}).get("lat"),
    "lon": el.get("lon") or el.get("center", {}).get("lon"),

    # contact
    "website": tags.get("website"),
    "phone": tags.get("phone"),
    "email": tags.get("email"),
}

                if business["website"]:
                    business["digital_status"] = "STRONG"
                    strong.append(business)
                else:
                    business["digital_status"] = "WEAK"
                    weak.append(business)

            return {
                "strong": strong[:limit],
                "weak": weak[:limit]
            }

        except Exception as e:

            return {
                "error": str(e),
                "strong": [],
                "weak": []
            }
