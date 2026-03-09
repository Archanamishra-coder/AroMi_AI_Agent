import bcrypt
import uuid
from db import get_connection

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(name, email, password, role, job_profession=None, locality=None, health_condition=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        user_uuid = str(uuid.uuid4())
        hashed_pw = hash_password(password)
        
        cursor.execute('''
        INSERT INTO Users (uuid, name, email, password_hash, role, job_profession, locality, health_condition)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_uuid, name, email, hashed_pw, role, job_profession, locality, health_condition))
        
        conn.commit()
        return True, user_uuid
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT uuid, name, password_hash, role FROM Users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user['password_hash']):
        return {
            'uuid': user['uuid'],
            'name': user['name'],
            'role': user['role']
        }
    return None

def get_user_profile(user_uuid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE uuid = ?', (user_uuid,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None
