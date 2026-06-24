from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, DateTime, Text
from datetime import datetime
from app.models.user import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    business_name: Mapped[str] = mapped_column(String, index=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    website: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)

    # Website analysis
    has_website: Mapped[bool] = mapped_column(default=False)
    https_enabled: Mapped[bool] = mapped_column(default=False)
    has_contact_page: Mapped[bool] = mapped_column(default=False)
    has_about_page: Mapped[bool] = mapped_column(default=False)
    has_services_page: Mapped[bool] = mapped_column(default=False)
    meta_title: Mapped[str] = mapped_column(String, nullable=True)
    meta_description: Mapped[str] = mapped_column(String, nullable=True)

    # Social media
    facebook: Mapped[str] = mapped_column(String, nullable=True)
    instagram: Mapped[str] = mapped_column(String, nullable=True)
    linkedin: Mapped[str] = mapped_column(String, nullable=True)
    twitter: Mapped[str] = mapped_column(String, nullable=True)
    tiktok: Mapped[str] = mapped_column(String, nullable=True)
    youtube: Mapped[str] = mapped_column(String, nullable=True)

    # Scoring
    score: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[str] = mapped_column(String, default="Low")
    score_explanation: Mapped[str] = mapped_column(Text, nullable=True)
    outreach_strategy: Mapped[str] = mapped_column(Text, nullable=True)

    # Meta
    source: Mapped[str] = mapped_column(String, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
