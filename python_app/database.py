import sqlite3
import os
import json

DB_PATH = os.path.join(os.getenv("APPDATA"), "PaperInk", "paperink.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sticky Notes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sticky_notes (
            id TEXT PRIMARY KEY,
            content TEXT,
            x INTEGER,
            y INTEGER,
            color TEXT
        )
    ''')

    # Tasks for Pomodoro Tree
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            completed BOOLEAN,
            created_date DATE DEFAULT CURRENT_DATE
        )
    ''')

    # App Usage Registry
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usage_minutes INTEGER DEFAULT 0,
            usage_date DATE DEFAULT CURRENT_DATE
        )
    ''')

    # Pomodoro Sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER,
            session_date DATE DEFAULT CURRENT_DATE
        )
    ''')

    conn.commit()
    conn.close()

# --- Sticky Notes Methods ---
def get_sticky_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, x, y, color FROM sticky_notes")
    notes = [{"id": row[0], "content": row[1], "x": row[2], "y": row[3], "color": row[4]} for row in cursor.fetchall()]
    conn.close()
    return notes

def save_sticky_note(note_id, content, x, y, color):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sticky_notes (id, content, x, y, color)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            content=excluded.content,
            x=excluded.x,
            y=excluded.y,
            color=excluded.color
    ''', (note_id, content, x, y, color))
    conn.commit()
    conn.close()

def delete_sticky_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sticky_notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# --- Task Methods ---
def get_daily_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks WHERE created_date = CURRENT_DATE")
    tasks = [{"id": row[0], "description": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return tasks

def add_task(description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, completed) VALUES (?, 0)", (description,))
    conn.commit()
    conn.close()

def update_task_status(task_id, completed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (int(completed), task_id))
    conn.commit()
    conn.close()

# --- Pomodoro Methods ---
def add_pomodoro_session(duration_minutes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pomodoro_sessions (duration_minutes) VALUES (?)", (duration_minutes,))
    conn.commit()
    conn.close()

def get_daily_pomodoro_minutes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(duration_minutes) FROM pomodoro_sessions WHERE session_date = CURRENT_DATE")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

# --- App Usage Methods ---
def add_usage_minute():
    conn = get_connection()
    cursor = conn.cursor()
    # Check if record for today exists
    cursor.execute("SELECT id FROM app_usage WHERE usage_date = CURRENT_DATE")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE app_usage SET usage_minutes = usage_minutes + 1 WHERE id = ?", (row[0],))
    else:
        cursor.execute("INSERT INTO app_usage (usage_minutes) VALUES (1)")
    conn.commit()
    conn.close()

def get_total_usage_minutes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(usage_minutes) FROM app_usage")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0
