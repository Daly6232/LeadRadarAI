from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import Lead

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    total = len(leads)
    strong = len([x for x in leads if x.score >= 80])
    weak = len([x for x in leads if x.score < 80])

    return {
        "total_leads": total,
        "strong_leads": strong,
        "weak_leads": weak,
        "conversion_rate": round((strong / total) * 100, 2) if total else 0,
    }
