import secrets
import sqlite3
from datetime import datetime, timedelta

from .database import get_connection


SESSION_DAYS = 30


def create_session(user_id):

    token = secrets.token_urlsafe(64)

    expires = (
        datetime.utcnow() +
        timedelta(days=SESSION_DAYS)
    ).isoformat()

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO sessions
        (
            token,
            user_id,
            expires_at
        )
        VALUES (?, ?, ?)
        """,
        (
            token,
            user_id,
            expires
        )
    )

    conn.commit()
    conn.close()

    return token


def get_session(token):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM sessions
        WHERE token=?
        """,
        (token,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    if datetime.fromisoformat(
        row["expires_at"]
    ) < datetime.utcnow():

        delete_session(token)

        return None

    return row


def delete_session(token):

    conn = get_connection()

    conn.execute(
        "DELETE FROM sessions WHERE token=?",
        (token,)
    )

    conn.commit()
    conn.close()