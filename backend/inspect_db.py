from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    print(conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")).fetchall())
    print(conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall())
