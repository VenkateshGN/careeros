import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("Error: DATABASE_URL not found in .env file.")
    exit(1)

# Mask password in printed URL for security
masked_url = db_url
if "@" in db_url:
    creds, host = db_url.split("@")
    if ":" in creds:
        prefix, pwd = creds.rsplit(":", 1)
        masked_url = f"{prefix}:******@{host}"

print(f"Connecting to database: {masked_url}\n")

engine = create_engine(db_url)

def show_summary():
    tables = ["users", "jobs", "applications", "agent_memories", "companies"]
    with engine.connect() as conn:
        for table in tables:
            try:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f" - Table '{table}': {count} records")
            except Exception as e:
                print(f" - Table '{table}': Could not read (Table may not exist yet)")

def inspect_table(table_name: str, limit: int = 10):
    print(f"\n--- First {limit} rows from '{table_name}' ---")
    with engine.connect() as conn:
        try:
            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
            keys = result.keys()
            rows = result.fetchall()
            if not rows:
                print("Table is empty.")
                return

            # Print headers
            header_str = " | ".join(keys)
            print(header_str)
            print("-" * len(header_str))

            # Print rows
            for row in rows:
                row_values = []
                for val in row:
                    val_str = str(val)
                    if len(val_str) > 50:
                        val_str = val_str[:47] + "..."
                    row_values.append(val_str)
                print(" | ".join(row_values))
        except Exception as e:
            print(f"Error querying table '{table_name}': {e}")

if __name__ == "__main__":
    show_summary()
    print("\nAvailable options to inspect:")
    print("1. Users\n2. Jobs\n3. Applications\n4. Agent Memories\n5. Exit")
    choice = input("\nEnter choice (1-5): ").strip()

    if choice == "1":
        inspect_table("users")
    elif choice == "2":
        inspect_table("jobs")
    elif choice == "3":
        inspect_table("applications")
    elif choice == "4":
        inspect_table("agent_memories")
    elif choice == "5":
        print("Goodbye!")
