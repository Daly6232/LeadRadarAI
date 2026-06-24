from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.lead_service import (
    get_all_leads,
    get_strong_leads,
    get_weak_leads,
    get_by_city,
    get_by_category,
    search_business,
)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/")
def list_leads(db: Session = Depends(get_db)):
    return get_all_leads(db)


@router.get("/strong")
def strong_leads(db: Session = Depends(get_db)):
    return get_strong_leads(db)


@router.get("/weak")
def weak_leads(db: Session = Depends(get_db)):
    return get_weak_leads(db)


@router.get("/city/{city}")
def leads_by_city(city: str, db: Session = Depends(get_db)):
    return get_by_city(db, city)


@router.get("/category/{category}")
def leads_by_category(category: str, db: Session = Depends(get_db)):
    return get_by_category(db, category)


@router.get("/search")
def search(
    q: str = Query(..., description="Business name"),
    db: Session = Depends(get_db)
):
    return search_business(db, q)
