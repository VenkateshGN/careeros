import sys
import os

# add backend path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.core.database import SessionLocal
from app.models.job import Job

db = SessionLocal()
try:
    jobs = db.query(Job).all()
    print("Jobs count:", len(jobs))
    for j in jobs:
        print(j.id, j.title)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
