import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "health_coach.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    columns_to_add = [
        ("dob", "DATE"),
        ("profession", "TEXT"),
        ("location", "TEXT"),
        ("profile_photo", "BLOB")
    ]
    
    # check existing columns
    c.execute("PRAGMA table_info(users)")
    existing_cols = [row[1] for row in c.fetchall()]
    
    for col_name, col_type in columns_to_add:
        if col_name not in existing_cols:
            c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added {col_name} to users table.")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
