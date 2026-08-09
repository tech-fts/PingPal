import time
import httpx
from app.config import settings

async def measure_latency() -> tuple[float, str]:
    """Measure HTTP response latency in milliseconds and return (latency, status) """
    async with httpx.AsyncClient(timeout=5.0) as client:
        start_time = time.perf_counter()
        try:
            response = await client.get("https://www.google.com") #error link 
            latency = (time.perf_counter() - start_time) * 1000

            if latency < 50:
                status = "green"
            elif latency < 150:
                status = "yellow"
            else:
                status = "red"

            return round(latency, 2), status
        except httpx.RequestError:
            return -1.0, "red"