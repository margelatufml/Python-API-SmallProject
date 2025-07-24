import sqlite3
from datetime import datetime
from typing import List
from .models import OperationRecord
import json

DB_PATH = 'math_microservice.db'

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
    conn.commit()
    conn.close()

def insert_operation(operation: str, input_data: dict, result: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO operations (operation, input_data, result, timestamp) VALUES (?, ?, ?, ?)',
        (
            operation,
            json.dumps(input_data),
            json.dumps(result),
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()

def list_operations() -> List[OperationRecord]:
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

# Inițializează DB la import
init_db()
