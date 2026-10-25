"""Simple SQLite key/value database helpers."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", Path(__file__).resolve().parent / "data.db")
)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS data (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.commit()


def setdata(key: str, value: Any) -> Any:
    if not isinstance(key, str) or not key.strip():
        raise ValueError("key must be a non-empty string")

    serialized = json.dumps(value)
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO data (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """ ,
            (key, serialized),
        )
        connection.commit()
    return value


def getdata(key: str) -> Any:
    with _connect() as connection:
        row = connection.execute(
            "SELECT value FROM data WHERE key = ?", (key,)
        ).fetchone()
    return None if row is None else json.loads(row["value"])


def create_user(username: str, password: str, token: str | list[str]) -> dict[str, Any]:
    """Create or replace a user record used by the WebSocket authenticator."""
    if not isinstance(username, str) or not username.strip():
        raise ValueError("username must be a non-empty string")
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    tokens = [token] if isinstance(token, str) else token
    if not tokens or not all(isinstance(item, str) and item for item in tokens):
        raise ValueError("token must be a non-empty string or list of strings")

    user = {"username": username, "password": password, "tokens": tokens}
    setdata(f"user:{username}", user)
    return user


def deletedata(key: str) -> bool:
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM data WHERE key = ?", (key,))
        connection.commit()
    return cursor.rowcount > 0


init_db()
