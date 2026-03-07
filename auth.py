import hashlib
import os
import uuid
from db import get_db_connection

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + key.hex()

def check_password(password, hashed):
    try:
        salt, key = hashed.split(':')
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000)
        return new_key.hex() == key
    except Exception:
        return False

def create_user(email, password, role="patient", name=""):
    conn = get_db_connection()
    c = conn.cursor()
    user_uuid = str(uuid.uuid4())
    hashed = hash_password(password)
    try:
        c.execute(
            "INSERT INTO users (uuid, email, password_hash, role, name) VALUES (?, ?, ?, ?, ?)",
            (user_uuid, email, hashed, role, name)
        )
        # If the user is an expert/admin, add to experts table too
        if role == "admin" or role == "expert":
            c.execute(
                "INSERT INTO experts (user_uuid) VALUES (?)",
                (user_uuid,)
            )
        conn.commit()
        return True, user_uuid
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT uuid, password_hash, role, name FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password(password, user['password_hash']):
        return {"uuid": user['uuid'], "role": user['role'], "name": user['name']}
    return None

def get_user_by_uuid(user_uuid):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT uuid, email, role, name FROM users WHERE uuid=?", (user_uuid,))
    user = c.fetchone()
    conn.close()
    if user:
         return dict(user)
    return None
