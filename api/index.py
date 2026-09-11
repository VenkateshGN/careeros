import os
import sys
from pathlib import Path

# Add backend directory to sys.path so app.* modules import cleanly
root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"

for p in [str(root_dir), str(backend_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app
