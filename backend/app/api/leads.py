from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import io

from app.database import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadOut, ScanRequest, DashboardStats
from app.services.scan_service import run_scan
from app.exporters.export_service import leads_to_csv, leads_to_json, leads_to_excel

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/", response_model=List[LeadOut])
def get_leads(
    skip: int = 0,
    limit: int = 50,
    city: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    min_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Lead)
    if city:
        q = q.filter(Lead.city.ilike(f"%{city}%"))
    if category:
        q = q.filter(Lead.category.ilike(f"%{category}%"))
    if priority:
        q = q.filter(Lead.priority == priority)
    if min_score is not None:
        q = q.filter(Lead.score >= min_score)
    return q.order_by(Lead.score.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=LeadOut)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    new_lead = Lead(**lead.model_dump())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Lead).count()
    high = db.query(Lead).filter(Lead.priority == "High").count()
    medium = db.query(Lead).filter(Lead.priority == "Medium").count()
    low = db.query(Lead).filter(Lead.priority == "Low").count()
    avg = db.query(func.avg(Lead.score)).scalar() or 0.0
    with_web = db.query(Lead).filter(Lead.has_website == True).count()
    without_web = db.query(Lead).filter(Lead.has_website == False).count()
    return DashboardStats(
        total_leads=total,
        high_priority=high,
        medium_priority=medium,
        low_priority=low,
        average_score=round(avg, 1),
        leads_with_website=with_web,
        leads_without_website=without_web,
    )


@router.post("/scan")
def scan_leads(req: ScanRequest, db: Session = Depends(get_db)):
    leads = run_scan(req.category, req.city, req.country, req.limit, db)
    return {
        "message": f"Scan complete. {len(leads)} new leads discovered.",
        "count": len(leads),
        "leads": [l.id for l in leads]
    }


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.score.desc()).all()
    content = leads_to_csv(leads)
    return StreamingResponse(
        io.StringIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=leadradar_leads.csv"}
    )


@router.get("/export/json")
def export_json_file(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.score.desc()).all()
    content = leads_to_json(leads)
    return StreamingResponse(
        io.StringIO(content),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=leadradar_leads.json"}
    )


@router.get("/export/excel")
def export_excel(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.score.desc()).all()
    content = leads_to_excel(leads)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=leadradar_leads.xlsx"}
    )


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"message": "Lead deleted"}
ENDOFFILE
