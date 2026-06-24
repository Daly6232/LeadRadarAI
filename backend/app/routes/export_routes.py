from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lead import Lead
from app.services.export_service import ExportService

router = APIRouter()
service = ExportService()


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    data = []

    for lead in leads:
        data.append({
            "business_name": lead.business_name,
            "category": lead.category,
            "city": lead.city,
            "website": lead.website,
            "phone": lead.phone,
            "email": lead.email,
            "score": lead.score,
            "ai_score": lead.ai_score,
            "ai_priority": lead.ai_priority,
            "ai_summary": lead.ai_summary,
        })

    filename = service.export_csv(data, "saved_leads")

    return {
        "status": "success",
        "file": filename,
        "total": len(data)
    }
