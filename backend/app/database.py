import aiosqlite
from app.config import settings

async def init_db():
    """Creates SQLite tables for devices and latency logs if they do not exist."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        # Table for storing discovered devices and nicknames
        await db.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                mac TEXT PRIMARY KEY,
                ip TEXT,
                name TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table for tracking internet health history
        await db.execute("""
            CREATE TABLE IF NOT EXISTS latency_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latency_ms REAL,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def log_latency(latency_ms: float, status: str):
    """Saves a ping test measurement into the database."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO latency_logs (latency_ms, status) VALUES (?, ?)",
            (latency_ms, status)
        )
        await db.commit()