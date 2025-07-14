import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn_str = (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASS')};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM Tasks")
    rows = cursor.fetchall()
    tasks = [{"id": row.id, "title": row.title, "status": row.status} for row in rows]
    conn.close()
    return tasks

def add_task(title, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks (title, status) VALUES (?, ?)", (title, status))
    conn.commit()
    conn.close()

def update_task(task_id, title, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Tasks SET title=?, status=? WHERE id=?", (title, status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
