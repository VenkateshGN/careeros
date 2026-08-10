class InterviewSimulationModelMock:
    def __init__(self, id, user_id, job_id, job_title, status, score, feedback, created_at):
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.job_title = job_title
        self.status = status
        self.score = score
        self.feedback = feedback
        self.created_at = created_at

# In a real app with SQLAlchemy:
# from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Text
# from app.core.database import Base
# class InterviewSimulation(Base):
#     __tablename__ = "interview_simulations"
#     id = Column(String, primary_key=True, index=True)
#     user_id = Column(String, ForeignKey("users.id"))
#     job_id = Column(String, nullable=True)
#     job_title = Column(String)
#     status = Column(String)
#     score = Column(Integer, nullable=True)
#     feedback = Column(Text, nullable=True)
#     created_at = Column(DateTime)
