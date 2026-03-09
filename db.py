import sqlite3
import os

DB_PATH = 'health_coach.db'

def get_connection():
    # Use check_same_thread=False for Streamlit's multi-threading model
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table (Patients and Admins/Experts)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('patient', 'admin', 'expert')),
        job_profession TEXT,
        locality TEXT,
        health_condition TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Medical History Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MedicalHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uuid TEXT NOT NULL,
        extracted_text TEXT,
        structured_data TEXT, -- JSON string of parsed LLM data
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_uuid) REFERENCES Users(uuid)
    )
    ''')
    
    # Nutrition Logs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NutritionLogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uuid TEXT NOT NULL,
        food_name TEXT,
        calories INTEGER,
        protein REAL,
        carbs REAL,
        fats REAL,
        source TEXT, -- 'manual', 'scan', 'voice'
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_uuid) REFERENCES Users(uuid)
    )
    ''')
    
    # AI Plans Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AIPlans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uuid TEXT NOT NULL,
        plan_type TEXT, -- 'nutrition', 'activity'
        plan_content TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_uuid) REFERENCES Users(uuid)
    )
    ''')

    # Expert Feedback Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uuid TEXT NOT NULL,
        expert_uuid TEXT NOT NULL,
        feedback_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_uuid) REFERENCES Users(uuid),
        FOREIGN KEY(expert_uuid) REFERENCES Users(uuid)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize upon import
init_db()
