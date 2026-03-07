import sqlite3
import uuid
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "health_coach.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medical History table
    c.execute('''
        CREATE TABLE IF NOT EXISTS medical_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_uuid TEXT NOT NULL,
            report_summary TEXT,
            conditions TEXT,
            allergies TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_uuid) REFERENCES users(uuid)
        )
    ''')
    
    # Food Logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_uuid TEXT NOT NULL,
            date DATE NOT NULL,
            food_item TEXT NOT NULL,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_uuid) REFERENCES users(uuid)
        )
    ''')

    # Experts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS experts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            specialization TEXT,
            availability TEXT,
            FOREIGN KEY(user_uuid) REFERENCES users(uuid)
        )
    ''')
    
    # Feedback table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expert_feedback (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             patient_uuid TEXT NOT NULL,
             expert_uuid TEXT NOT NULL,
             feedback_text TEXT,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY(patient_uuid) REFERENCES users(uuid),
             FOREIGN KEY(expert_uuid) REFERENCES users(uuid)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
