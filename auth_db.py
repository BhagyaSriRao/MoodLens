import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, Tuple, Any

DB_PATH = "auth.db"


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables for users, sessions, and emotion_logs if they do not exist."""
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_time TEXT NOT NULL,
            logout_time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER,
            source_type TEXT NOT NULL,        -- 'text' or 'file'
            source_text TEXT,
            file_name TEXT,
            predicted_emotion TEXT,
            extra TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
        """
    )

    conn.commit()
    conn.close()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    """Create a new user. Returns (success, error_message)."""
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, _hash_password(password), datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another one."
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[sqlite3.Row]:
    """Return the user row if credentials are valid, otherwise None."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
    row = cur.fetchone()
    conn.close()

    if row and row["password_hash"] == _hash_password(password):
        return row
    return None


def start_session(user_id: int) -> int:
    """Insert a new session row and return its ID."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sessions (user_id, login_time) VALUES (?, ?)",
        (user_id, datetime.utcnow().isoformat()),
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()
    return session_id


def end_session(session_id: int) -> None:
    """Set logout_time for a session."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE sessions SET logout_time = ? WHERE id = ? AND logout_time IS NULL",
        (datetime.utcnow().isoformat(), session_id),
    )
    conn.commit()
    conn.close()


def log_emotion(
    user_id: int,
    session_id: Optional[int],
    source_type: str,
    source_text: Optional[str] = None,
    file_name: Optional[str] = None,
    predicted_emotion: Optional[str] = None,
    extra: Optional[str] = None,
) -> None:
    """Insert a row into emotion_logs."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO emotion_logs (
            user_id, session_id, source_type, source_text,
            file_name, predicted_emotion, extra, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            session_id,
            source_type,
            source_text,
            file_name,
            predicted_emotion,
            extra,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
