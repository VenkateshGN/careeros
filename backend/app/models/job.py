import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base, GUID


class Job(Base):
    __tablename__ = "jobs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    company_id = Column(GUID, ForeignKey("companies.id"), nullable=True)
    recruiter_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    location = Column(String(200), nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)

    posted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    company = relationship("Company", lazy="joined")

    @property
    def company_name(self):
        return self.company.name if self.company else "CareerOS Partner"

    @property
    def company_logo(self):
        return self.company.logo_url if self.company else None

    @property
    def company_website(self):
        return self.company.website if self.company else None
