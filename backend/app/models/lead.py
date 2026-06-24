from sqlalchemy import Column, Integer, String
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    business_name = Column(String, nullable=False)
    category = Column(String)
    city = Column(String)

    website = Column(String)
    phone = Column(String)
    email = Column(String)

    score = Column(Integer, default=0)

    # 🧠 AI FIELDS (Phase 4.2+)
    ai_score = Column(Integer, nullable=True)
    ai_priority = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)
