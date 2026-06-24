from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lead import Lead
from app.scrapers.osm_scraper import OSMScraper

router = APIRouter()
scraper = OSMScraper()


class ScanRequest(BaseModel):
    category: str
    city: str
    limit: int = 10


@router.post("/scan/osm")
def scan_osm(data: ScanRequest, db: Session = Depends(get_db)):

    # 1. Run scraper
    results = scraper.search(
        category=data.category,
        city=data.city,
        limit=data.limit
    )

    if "error" in results:
        return results

    strong = results.get("strong", [])
    weak = results.get("weak", [])

    all_leads = strong + weak

    saved = 0
    duplicates = 0

    # 2. Process each lead
    for item in all_leads:

        business_name = item["name"]
        if not business_name:
            continue

        # 3. Skip duplicates
        exists = db.query(Lead).filter(
            Lead.business_name == business_name
        ).first()

        if exists:
            duplicates += 1
            continue

        # 4. Extract fields
        website = item.get("website")
        phone = item.get("phone")
        email = item.get("email")

        # 5. Score calculation
        score = 0

        if website:
            score += 50

        if phone:
            score += 30

        if email:
            score += 20

        # 6. Create DB object
        lead = Lead(
            business_name=business_name,
            category=item.get("category"),
            city=item.get("city"),
            website=website,
            phone=phone,
            email=email,
            score=score
        )

        # 7. Save to DB
        db.add(lead)
        saved += 1

    # 8. Commit once at end
    db.commit()

    # 9. Response
    return {
        "saved": saved,
        "duplicates": duplicates,
        "strong": len(strong),
        "weak": len(weak)
    }
