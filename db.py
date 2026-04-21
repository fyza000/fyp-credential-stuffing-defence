import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = Path("events.db") # Local SQLite database file

def _connect() -> sqlite3.Connection: 
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts_utc TEXT NOT NULL,
                username TEXT,
                ip TEXT,
                user_agent TEXT,
                risk_score INTEGER NOT NULL,
                decision TEXT NOT NULL,
                reasons TEXT NOT NULL
            )
        """)
        conn.commit()

def log_event(
    username: Optional[str],
    ip: str,
    user_agent: Optional[str],
    risk_score: int,
    decision: str,
    reasons: List[str],
) -> None:
    reasons_str = "; ".join(reasons) if reasons else "None"
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO login_events (ts_utc, username, ip, user_agent, risk_score, decision, reasons)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (datetime.utcnow().isoformat(), username, ip, user_agent, risk_score, decision, reasons_str),
        )
        conn.commit()

def latest_events(limit: int = 20) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM login_events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
