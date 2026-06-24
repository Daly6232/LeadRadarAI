from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.services.ai_service import analyze_lead


def analyze_all_leads(db: Session):
    leads = db.query(Lead).all()

    results = []
    failed = 0

    for lead in leads:
        try:
            analysis = analyze_lead(lead)

            lead.ai_score = analysis["score"]
            lead.ai_priority = analysis["priority"]
            lead.ai_summary = analysis["summary"]

            results.append(analysis)

        except Exception:
            failed += 1
            continue

    db.commit()

    return {
        "status": "success",
        "total_analyzed": len(results),
        "failed": failed,
        "high_quality": len([r for r in results if r["priority"] == "High"]),
        "low_quality": len([r for r in results if r["priority"] == "Low"]),
        "results": results
    }
