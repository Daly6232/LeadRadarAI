from sqlalchemy.orm import Session
from app.models.lead import Lead


def get_all_leads(db: Session):
    return db.query(Lead).order_by(Lead.score.desc()).all()


def get_strong_leads(db: Session):
    return db.query(Lead).filter(Lead.score >= 50).all()


def get_weak_leads(db: Session):
    return db.query(Lead).filter(Lead.score < 50).all()


def get_by_city(db: Session, city: str):
    return db.query(Lead).filter(Lead.city == city).all()


def get_by_category(db: Session, category: str):
    return db.query(Lead).filter(Lead.category == category).all()


def search_business(db: Session, keyword: str):
    return db.query(Lead).filter(
        Lead.business_name.ilike(f"%{keyword}%")
    ).all()
