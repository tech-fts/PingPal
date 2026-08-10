from pathlib import Path
from pydantic_settings import BaseSettings

# Define base directory (root directory of your project/app)
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    SUBNET_RANGE: str = "192.168.1.0/24"
    PING_INTERVAL: int = 15
    LATENCY_TEST_URL: str = "https://www.google.com"

    # Path to the SQLite database file
    DATABASE_PATH: Path = BASE_DIR / "data" / "app.db"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure target directory exists before running the app
settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)