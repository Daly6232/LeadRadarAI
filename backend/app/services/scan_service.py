"""
Orchestrates: scrape → analyze → score → save
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.scrapers.osm_scraper import scrape_businesses
from app.analyzers.website_analyzer import analyze_website
from app.scoring.lead_scorer import score_lead
from app.models.lead import Lead
from typing import List, Dict


def run_scan(category: str, city: str, country: str, limit: int, db: Session) -> List[Dict]:
    """Full pipeline: discover → analyze → score → persist"""
    businesses = scrape_businesses(category, city, country, limit)
    results = []

    for biz in businesses:
        # Skip if already exists
        existing = db.query(Lead).filter(
            Lead.business_name == biz["business_name"],
            Lead.city == biz.get("city", city)
        ).first()
        if existing:
            continue

        # Analyze website if available
        analysis = {}
        if biz.get("website"):
            analysis = analyze_website(biz["website"])
        else:
            analysis = {
                "has_website": False,
                "https_enabled": False,
                "has_contact_page": False,
                "has_about_page": False,
                "has_services_page": False,
                "meta_title": None,
                "meta_description": None,
                "email": biz.get("email"),
                "phone": biz.get("phone"),
                "facebook": None,
                "instagram": None,
                "linkedin": None,
                "twitter": None,
                "tiktok": None,
                "youtube": None,
            }

        # Merge data
        merged = {**biz, **analysis}
        # Prefer OSM contact data if analyzer didn't find any
        if not merged.get("email") and biz.get("email"):
            merged["email"] = biz["email"]
        if not merged.get("phone") and biz.get("phone"):
            merged["phone"] = biz["phone"]

        # Score
        score, priority, explanation, strategy = score_lead(merged)

        # Save
        lead = Lead(
            business_name=merged.get("business_name", "Unknown"),
            category=category,
            website=merged.get("website"),
            email=merged.get("email"),
            phone=merged.get("phone"),
            city=merged.get("city") or city,
            country=merged.get("country") or country,
            address=merged.get("address"),
            has_website=merged.get("has_website", False),
            https_enabled=merged.get("https_enabled", False),
            has_contact_page=merged.get("has_contact_page", False),
            has_about_page=merged.get("has_about_page", False),
            has_services_page=merged.get("has_services_page", False),
            meta_title=merged.get("meta_title"),
            meta_description=merged.get("meta_description"),
            facebook=merged.get("facebook"),
            instagram=merged.get("instagram"),
            linkedin=merged.get("linkedin"),
            twitter=merged.get("twitter"),
            tiktok=merged.get("tiktok"),
            youtube=merged.get("youtube"),
            score=score,
            priority=priority,
            score_explanation=explanation,
            outreach_strategy=strategy,
            source="openstreetmap",
            analyzed_at=datetime.utcnow(),
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        results.append(lead)

    return results
