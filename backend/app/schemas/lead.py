from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    business_name: str
    category: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    business_name: str
    category: Optional[str]
    website: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    country: Optional[str]
    address: Optional[str]
    has_website: bool
    https_enabled: bool
    has_contact_page: bool
    has_about_page: bool
    has_services_page: bool
    meta_title: Optional[str]
    meta_description: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    linkedin: Optional[str]
    twitter: Optional[str]
    tiktok: Optional[str]
    youtube: Optional[str]
    score: float
    priority: str
    score_explanation: Optional[str]
    outreach_strategy: Optional[str]
    source: str
    created_at: datetime
    analyzed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ScanRequest(BaseModel):
    category: str
    city: str
    country: str
    limit: int = 20


class DashboardStats(BaseModel):
    total_leads: int
    high_priority: int
    medium_priority: int
    low_priority: int
    average_score: float
    leads_with_website: int
    leads_without_website: int
