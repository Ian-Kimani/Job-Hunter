import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'jobs.db')

def init_db():
    """Initializes the database and creates the seen_jobs table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seen_jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            source TEXT,
            date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_job_seen(job_id: str) -> bool:
    """Checks if a job URL or ID has already been seen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM seen_jobs WHERE id = ?', (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_job(job_id: str, title: str, company: str, source: str):
    """Saves a new job to the database so we don't alert on it again."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO seen_jobs (id, title, company, source)
            VALUES (?, ?, ?, ?)
        ''', (job_id, title, company, source))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already exists
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
