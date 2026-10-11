import os
import sys
from pathlib import Path
from sqlalchemy import text

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine

def load_seed(sql_file_path: str = "seed_data.sql"):
    if not os.path.exists(sql_file_path):
        print(f"Error: {sql_file_path} not found.")
        return False

    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    with engine.begin() as connection:
        # Guard: Check if database is empty
        note_count = connection.execute(text("SELECT count(*) FROM notes;")).scalar() or 0
        if note_count > 0:
            print(f"[REFUSED] Database is NOT empty (contains {note_count} existing notes).")
            print("Seed data can only be loaded into an empty database to protect your data.")
            return False

        print(f"Database is empty. Loading seed data from {sql_file_path}...")
        statements = sql_content.split(";")
        for stmt in statements:
            cleaned = stmt.strip()
            if cleaned:
                connection.execute(text(cleaned))

    print("Seed data successfully loaded!")
    return True

if __name__ == "__main__":
    success = load_seed()
    if not success:
        sys.exit(1)
