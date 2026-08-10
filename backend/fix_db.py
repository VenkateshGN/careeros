from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from app.core.database import Base

from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.models.company import Company
from app.models.builder import BuiltResume
from app.models.password_reset import PasswordReset

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))
        
Base.metadata.create_all(engine)
print("Sprint 15 AI Resume Builder Tables generated successfully.")
