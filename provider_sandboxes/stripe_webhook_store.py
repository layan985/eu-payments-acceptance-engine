import sqlite3
import time


SCHEMA = """
CREATE TABLE IF NOT EXISTS stripe_webhook_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    object_id TEXT,
    processing_state TEXT NOT NULL,
    received_at INTEGER NOT NULL,
    processed_at INTEGER
)
"""


class EventStore:
    """Small SQLite-backed idempotency ledger for Stripe webhook events."""

    def __init__(self, path="stripe_webhook_events.db"):
        self.path = path
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as connection:
            connection.execute(SCHEMA)

    def claim(self, event_summary, now=None):
        event_id = event_summary.get("event_id")
        event_type = event_summary.get("event_type")
        if not event_id or not event_type:
            raise ValueError("event_id and event_type are required")

        received_at = int(time.time() if now is None else now)
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO stripe_webhook_events
                        (event_id, event_type, object_id, processing_state, received_at)
                    VALUES (?, ?, ?, 'processing', ?)
                    """,
                    (
                        event_id,
                        event_type,
                        event_summary.get("object_id"),
                        received_at,
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def mark_processed(self, event_id, now=None):
        processed_at = int(time.time() if now is None else now)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE stripe_webhook_events
                SET processing_state = 'processed', processed_at = ?
                WHERE event_id = ?
                """,
                (processed_at, event_id),
            )
        if cursor.rowcount != 1:
            raise KeyError(f"unknown event_id: {event_id}")

    def mark_failed(self, event_id):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE stripe_webhook_events
                SET processing_state = 'failed'
                WHERE event_id = ?
                """,
                (event_id,),
            )
        if cursor.rowcount != 1:
            raise KeyError(f"unknown event_id: {event_id}")

    def get(self, event_id):
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT event_id, event_type, object_id, processing_state,
                       received_at, processed_at
                FROM stripe_webhook_events
                WHERE event_id = ?
                """,
                (event_id,),
            ).fetchone()
        return dict(row) if row else None
