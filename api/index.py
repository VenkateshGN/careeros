import sys
import traceback
from pathlib import Path
from fastapi import FastAPI

root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"

for p in [str(root_dir), str(backend_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.main import app
except Exception as e:
    err_str = f"Import Error: {e}\n{traceback.format_exc()}"
    app = FastAPI()
    
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    def err_fallback(full_path: str):
        return {"error": True, "detail": err_str}
