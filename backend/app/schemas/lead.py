from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadCreate(BaseModel):
    business_name: str
    category: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class LeadResponse(LeadCreate):
    id: int
    score: int

    class Config:
        from_attributes = True
