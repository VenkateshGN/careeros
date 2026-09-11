import os
import sys
from pathlib import Path

# Ensure backend root directory is in sys.path for Vercel Serverless
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if "." not in sys.path:
    sys.path.insert(0, ".")

from app.main import app
