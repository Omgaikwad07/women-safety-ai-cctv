# alert_system/database.py

import sqlite3
from datetime import datetime

DB_NAME = "alert_system/alerts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        threat_score REAL,
        snapshot TEXT,
        video TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_alert(threat_score, snapshot_path, video_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO alerts (timestamp, threat_score, snapshot, video)
    VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        threat_score,
        snapshot_path,
        video_path
    ))

    conn.commit()
    conn.close()


def get_latest_alerts(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, timestamp, threat_score, snapshot, video
        FROM alerts
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "timestamp": r[1],
            "threat_score": r[2],
            "snapshot": r[3],
            "video": r[4]
        })

    return results
