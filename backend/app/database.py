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

async def get_known_devices() -> dict[str, dict]:
    """Retrieves all known devices from the database, keyed by MAC address."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        cursor = await db.execute("SELECT mac, ip, name, first_seen, last_seen FROM devices")
        rows = await cursor.fetchall()
        return {
            row[0]: {
                "mac": row[0],
                "ip": row[1],
                "name": row[2],
                "first_seen": row[3],
                "last_seen": row[4]
            }
            for row in rows
        }

async def save_device(mac: str, ip: str, name: str = ""):
    """Saves a discovered device into the database."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO devices (mac, ip, name, last_seen)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(mac) DO UPDATE SET
                ip=excluded.ip,
                name=excluded.name,
                last_seen=CURRENT_TIMESTAMP
            """,
            (mac, ip, name)
        )
        await db.commit()

async def get_recent_latency_logs(limit: int = 10) -> list[dict]:
    """Retrieves the most recent latency logs from the database."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT latency_ms, status, timestamp FROM latency_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        return [
            {
                "latency_ms": row[0],
                "status": row[1],
                "timestamp": row[2]
            }
            for row in rows
        ]