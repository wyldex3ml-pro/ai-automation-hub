import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "data/leads.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            category TEXT,
            priority TEXT,
            sentiment TEXT,
            summary TEXT,
            suggested_reply TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            replied INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialised successfully.")

def save_lead(sender, subject, body, classification, reply):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads 
        (sender, subject, body, category, priority, sentiment, summary, suggested_reply)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sender,
        subject,
        body,
        classification.get("category"),
        classification.get("priority"),
        classification.get("sentiment"),
        classification.get("summary"),
        reply
    ))
    conn.commit()
    conn.close()

def get_all_leads():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY processed_at DESC")
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return leads

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM leads 
        GROUP BY category
    """)
    stats = dict(cursor.fetchall())
    cursor.execute("SELECT COUNT(*) FROM leads")
    stats["total"] = cursor.fetchone()[0]
    conn.close()
    return stats

if __name__ == "__main__":
    init_db()
    print("Stats:", get_stats())