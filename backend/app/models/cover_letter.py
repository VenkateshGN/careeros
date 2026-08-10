class CoverLetterModelMock:
    def __init__(self, id, user_id, job_id, company_name, job_title, content, tone, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.company_name = company_name
        self.job_title = job_title
        self.content = content
        self.tone = tone
        self.created_at = created_at
        self.updated_at = updated_at

# In a real app with SQLAlchemy:
# from sqlalchemy import Column, String, ForeignKey, DateTime
# from app.core.database import Base
# class CoverLetter(Base):
#     __tablename__ = "cover_letters"
#     id = Column(String, primary_key=True, index=True)
#     user_id = Column(String, ForeignKey("users.id"))
#     job_id = Column(String, nullable=True)
#     company_name = Column(String)
#     job_title = Column(String)
#     content = Column(String)
#     tone = Column(String)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
