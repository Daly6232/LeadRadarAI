from app.services.analyzer.fetcher import fetch_website

result = fetch_website("https://example.com")

print("Status:", result["status"])
print("Title:", result["soup"].title.string)
