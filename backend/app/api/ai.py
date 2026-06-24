from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lead import Lead
from app.services.ai_service import analyze_lead
from app.services.ai_bulk import analyze_all_leads

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/lead/{lead_id}")
def analyze_single_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = db.query(Lead).filter(
        Lead.id == lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return analyze_lead(lead)


@router.post("/analyze")
def bulk_analyze(db: Session = Depends(get_db)):
    return analyze_all_leads(db)


@router.get("/stats")
def ai_stats(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    total = len(leads)
    analyzed = len([l for l in leads if l.score is not None])

    if analyzed == 0:
        return {
            "total_leads": total,
            "analyzed": 0,
            "high_quality": 0,
            "average_score": 0
        }

    high_quality = len([
        l for l in leads
        if l.score is not None and l.score >= 70
    ])

    average_score = round(
        sum(l.score for l in leads if l.score is not None)
        / analyzed,
        2
    )

    return {
        "total_leads": total,
        "analyzed": analyzed,
        "high_quality": high_quality,
        "average_score": average_score
    }
