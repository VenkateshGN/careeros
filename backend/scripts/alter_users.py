import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine

def apply_migrations():
    print("Applying missing columns to users table...")
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'candidate' NOT NULL;"))
            print("Successfully added: 'role'")
        except Exception as e:
            print(f"Skipped 'role' (might already exist) -> {e}")

        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN organization_id VARCHAR(100);"))
            print("Successfully added: 'organization_id'")
        except Exception as e:
            print(f"Skipped 'organization_id' (might already exist) -> {e}")

    print("Database sync complete!")

if __name__ == "__main__":
    apply_migrations()
