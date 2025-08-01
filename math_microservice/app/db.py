
import sqlite3
from datetime import datetime
from typing import List
from .models import OperationRecord
import json
import os

# Alternative persistence config
PERSISTENCE_MODE = os.environ.get("PERSISTENCE_MODE", "sqlite")  # sqlite, memory, file
DB_PATH = 'math_microservice.db'
FILE_PATH = 'math_microservice_ops.json'
_memory_ops = []

import hashlib
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            input_data TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            name TEXT PRIMARY KEY,
            description TEXT
        )
    ''')
    # Default admin user
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                  ('admin', hash_password('admin'), 'admin'))
    conn.commit()
    conn.close()

def insert_operation(operation: str, input_data: dict, result: dict):
    timestamp = datetime.utcnow().isoformat()
    if PERSISTENCE_MODE == "sqlite":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            'INSERT INTO operations (operation, input_data, result, timestamp) VALUES (?, ?, ?, ?)',
            (
                operation,
                json.dumps(input_data),
                json.dumps(result),
                timestamp
            )
        )
        conn.commit()
        conn.close()
    elif PERSISTENCE_MODE == "memory":
        _memory_ops.append(OperationRecord(
            id=len(_memory_ops)+1,
            operation=operation,
            input_data=json.dumps(input_data),
            result=json.dumps(result),
            timestamp=datetime.fromisoformat(timestamp)
        ))
    elif PERSISTENCE_MODE == "file":
        try:
            with open(FILE_PATH, "r") as f:
                ops = json.load(f)
        except Exception:
            ops = []
        ops.append({
            "id": len(ops)+1,
            "operation": operation,
            "input_data": json.dumps(input_data),
            "result": json.dumps(result),
            "timestamp": timestamp
        })
        with open(FILE_PATH, "w") as f:
            json.dump(ops, f)

def list_operations() -> List[OperationRecord]:
    if PERSISTENCE_MODE == "sqlite":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, operation, input_data, result, timestamp FROM operations ORDER BY id DESC')
        rows = c.fetchall()
        conn.close()
        return [
            OperationRecord(
                id=row[0],
                operation=row[1],
                input_data=row[2],
                result=row[3],
                timestamp=datetime.fromisoformat(row[4])
            ) for row in rows
        ]
    elif PERSISTENCE_MODE == "memory":
        return list(reversed(_memory_ops))
    elif PERSISTENCE_MODE == "file":
        try:
            with open(FILE_PATH, "r") as f:
                ops = json.load(f)
        except Exception:
            ops = []
        return [
            OperationRecord(
                id=op["id"],
                operation=op["operation"],
                input_data=op["input_data"],
                result=op["result"],
                timestamp=datetime.fromisoformat(op["timestamp"])
            ) for op in reversed(ops)
        ]

# Inițializează DB la import
# Inițializează DB la import

# User CRUD
def create_user(username: str, password: str, role: str = "user"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
              (username, password_hash, role))
    conn.commit()
    conn.close()

def get_user(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return row

def verify_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False, None
    password_hash = hash_password(password)
    if user[2] == password_hash:
        return True, user[3]
    return False, None

def get_user_role(username: str):
    user = get_user(username)
    if user:
        return user[3]
    return None

init_db()
