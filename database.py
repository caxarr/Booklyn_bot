from dataclasses import dataclass
from datetime import datetime, timezone

import aiosqlite

from config import DB_PATH

STATUS_PENDING = "pending"
STATUS_CONFIRMED = "confirmed"
STATUS_CANCELLED = "cancelled"

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL
)
"""


@dataclass
class Booking:
    id: int
    user_id: int
    username: str | None
    name: str
    date: str
    time: str
    description: str
    status: str
    created_at: str


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(_CREATE_TABLE_SQL)
        await db.commit()


async def add_booking(
    user_id: int,
    username: str | None,
    name: str,
    date: str,
    time: str,
    description: str,
) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO bookings (user_id, username, name, date, time, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, name, date, time, description, STATUS_PENDING, created_at),
        )
        await db.commit()
        return cursor.lastrowid


async def get_user_bookings(user_id: int) -> list[Booking]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT * FROM bookings
            WHERE user_id = ? AND status != ?
            ORDER BY created_at DESC
            """,
            (user_id, STATUS_CANCELLED),
        )
        rows = await cursor.fetchall()
        return [Booking(**dict(row)) for row in rows]


async def get_all_bookings() -> list[Booking]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        return [Booking(**dict(row)) for row in rows]
